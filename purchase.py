import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

# 저장된 모델 및 전처리기 로드
knn_model = joblib.load("knn_model_no_year.pkl")  # KNN 모델 로드 함수 사용
preprocessor = joblib.load("preprocessor.pkl")  # 전처리기 로드



def predict_yield(avg_temp, df):
    
    average_rain_fall_mm_per_year = 1405
    avg_temp = 16.07
    # 입력 데이터 생성
    input_data = pd.DataFrame([[average_rain_fall_mm_per_year, avg_temp, 'Maize']], 
                              columns=['avg_temp', 'Item'])

    # 전처리 적용
    processed_data = preprocessor.transform(input_data)

    # 수확량 예측
    predicted_yield = knn_model.predict(processed_data)[0]
    print(predicted_yield)
    
    # 상위 퍼센트 계산 (이미 있는 데이터를 기준으로)
    item_yields = df[df['Item'] == item]['hg/ha_yield'].sort_values().values
    rank_percentile = np.sum(item_yields < predicted_yield) / len(item_yields) * 100

    return rank_percentile

# 데이터셋 로드 (예: 테스트 데이터셋 또는 새 데이터셋)


# 함수 사용 예시
#predicted_yield, rank_percentile = predict_yield(16.37, 'Maize', df)
print(f"Predicted Yield: {predicted_yield} kg/ha")
print(f"Predicted Yield is in the top {rank_percentile:.2f}% for Maize")
