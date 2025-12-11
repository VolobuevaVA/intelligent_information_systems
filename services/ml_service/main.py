from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging
import time
from api_handler import FastAPIHandler
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

# Инициализация метрик
PREDICTION_PRICE = Histogram(
    'prediction_price',
    'Price predictions distribution',
    buckets=(0, 5, 10, 15, 20, 25, 30, 40, 50, float('inf'))
)

REQUEST_COUNT = Counter(
    'request_count',
    'App Request Count',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'request_latency_seconds',
    'Request latency',
    ['endpoint']
)

# Middleware для сбора метрик
class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        method = request.method
        endpoint = request.url.path
        
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(process_time)
        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            http_status=response.status_code
        ).inc()
        
        return response

app = FastAPI(title="Car Price Prediction Service", version="2.0")

# Добавляем middleware
app.add_middleware(MetricsMiddleware)

# Инициализируем обработчик API
api_handler = FastAPIHandler()

class Features(BaseModel):
    features: List[float]

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/api/prediction")
async def predict(item_id: int, features: Features):
    try:
        if len(features.features) != 7:
            raise HTTPException(status_code=400, detail="Expected 7 features")
        
        # Используем реальную модель для предсказания
        prediction = api_handler.predict(features.features)
        
        # Сохраняем метрику
        PREDICTION_PRICE.observe(prediction)
        
        return {
            "item_id": item_id,
            "price": prediction
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))