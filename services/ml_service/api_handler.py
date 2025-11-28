import pickle
import pandas as pd
from typing import List
import logging
import os

logger = logging.getLogger("uvicorn.error")

class FastAPIHandler:
    def __init__(self, model_path: str = "/ml_service/model_fixed.pkl"):
        self.model = None
        self.model_path = model_path
        self.load_model()
    
    def load_model(self):
        try:
            logger.info(f"Загружаем модель из {self.model_path}")
            
            if not os.path.exists(self.model_path):
                logger.error(f"Файл модели не найден: {self.model_path}")
                return
            
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            logger.info("Модель успешно загружена")
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке модели: {e}")
            self.model = None
    
    def predict(self, features: List[float]) -> float:
        if self.model is None:
            logger.info(f'Модель не загружена')
            return 0.0
        
        try:
            features_df = pd.DataFrame([{
                'Present_Price': float(features[0]),
                'Driven_kms': int(features[1]),
                'Fuel_Type': str(int(features[2])),
                'Selling_type': str(int(features[3])),
                'Transmission': str(int(features[4])),
                'Year_Category': str(int(features[5])),
                'Car_Frequency_Category': str(int(features[6]))
            }])
            
            prediction = self.model.predict(features_df)
            return float(prediction[0])
            
        except Exception as e:
            logger.error(f"Ошибка при предсказании: {e}")
            return 0.0