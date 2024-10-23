from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
import random
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # CORS 활성화

# MongoDB 연결 설정
MONGO_URI = "mongodb://farmos:taehyun@farmos-db:27017/farmosdb"
client = MongoClient(MONGO_URI)
db = client['farmosdb']
collection = db['photos']

# 업로드 폴더 설정
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# TODO: 메소드 1 구현부분: 사진을 통한 질병데이터 생성
def generate_score():
    return random.randint(1, 10)

# TODO: 메소드 2 구현부분: 센서 데이터를 통한 결과
def generate_score_by_sensor(sensor1, sensor2, sensor3):
    return random.randint(1, 10)


# 파일 업로드 엔드포인트
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'farm_id' not in request.form:
        return jsonify({'error': 'JPEG 파일과 농장 ID가 필요합니다.'}), 400

    file = request.files['file']
    farm_id = request.form['farm_id']

    if not file.filename.endswith(('.jpg', '.jpeg')):
        return jsonify({'error': 'JPEG 형식의 파일만 허용됩니다.'}), 400

    # 고유한 파일 이름 생성 및 저장
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    # TODO: 메소드1 사용위치
    score = generate_score()

    document = {
        'farm_id': farm_id,
        'filename': filename,
        'uploaded_at': datetime.now()
    }
    collection.insert_one(document)

    return jsonify({
        'message': '파일 업로드 성공',
        'farm_id': farm_id,
        'filename': filename,
        'score': score
    }), 200

# 센서 데이터에 기반한 점수 반환 엔드포인트
@app.route('/sensor-score', methods=['POST'])
def sensor_score():
    try:
        # TODO: 원하는 센서데이터 갯수만큼 조절하기
        sensor1 = float(request.json.get('sensor1'))
        sensor2 = float(request.json.get('sensor2'))
        sensor3 = float(request.json.get('sensor3'))

        # TODO: 메소드2 사용위치
        score = generate_score_by_sensor(sensor1,sensor2,sensor3) # 1~10 사이로 제한

        return jsonify({
            'score': score
        }), 200

    except (ValueError, TypeError):
        return jsonify({'error': '잘못된 센서 데이터입니다. float형 데이터를 제공해야 합니다.'}), 400

# Flask 애플리케이션 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

