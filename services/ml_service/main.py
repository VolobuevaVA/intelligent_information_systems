from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from api_handler import FastAPIHandler

# Создаем экземпляр FastAPI-приложения
app = FastAPI(title="ML Service")

# Инициализируем обработчик API
api_handler = FastAPIHandler()

# Модель данных для входных признаков
class Features(BaseModel):
    features: List[float]

# Обработчик GET-запросов к корню "/"
@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Endpoint для предсказаний
@app.post("/api/prediction")
async def predict(item_id: int, features: Features):
    """
    Возвращает предсказание для объекта
    
    - **item_id**: идентификатор объекта
    - **features**: список признаков для предсказания
    """
    # Используем реальную модель для предсказания
    prediction = api_handler.predict(features.features)
    
    return {
        "item_id": item_id,
        "price": prediction
    }