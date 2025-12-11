import json
import time
import random
import logging
import os
import urllib.request
import urllib.error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PREDICTION_SERVICE_URL = os.getenv("PREDICTION_SERVICE_URL", "http://localhost:8000")

def generate_random_data():
    """Генерация случайных данных для предсказания"""
    return {
        "features": [
            round(random.uniform(1, 30), 1),  # Present_Price
            random.randint(1000, 200000),     # Driven_kms
            random.randint(0, 1),             # Fuel_Type
            random.randint(0, 1),             # Selling_type
            random.randint(0, 1),             # Transmission
            random.randint(1, 3),             # Year_Category
            random.randint(1, 3)              # Car_Frequency_Category
        ]
    }

def send_request():
    """Отправка запроса к сервису предсказаний"""
    try:
        item_id = random.randint(1, 1000)
        data = generate_random_data()
        
        url = f"{PREDICTION_SERVICE_URL}/api/prediction?item_id={item_id}"
        headers = {'Content-Type': 'application/json'}
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            logger.info(f"Request successful: {result}")
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.readable() else ''
        logger.error(f"HTTP Error {e.code}: {e.reason} - {error_body}")
    except Exception as e:
        logger.error(f"Error: {e}")

def main():
    """Основной цикл отправки запросов"""
    logger.info(f"Starting request service. Target: {PREDICTION_SERVICE_URL}")
    
    while True:
        send_request()
        sleep_time = random.uniform(0, 5)
        logger.debug(f"Sleeping for {sleep_time:.2f} seconds")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()