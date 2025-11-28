import mlflow
import pickle
import os

def download_model(run_id, output_path="model.pkl"):
    """
    Загружает модель из MLflow по run_id и сохраняет в файл
    
    Args:
        run_id (str): ID прогона в MLflow
        output_path (str): Путь для сохранения модели
    """
    try:
        #адрес MLflow сервера
        mlflow.set_tracking_uri("http://localhost:5000")
        
        print(f"Подключаемся к MLflow: http://localhost:5000")
        print(f"Загружаем модель с run_id: {run_id}")
        
        # Скачиваем артефакт модели
        model_uri = f"runs:/{run_id}/model"
        model = mlflow.pyfunc.load_model(model_uri)
        
        # Сохраняем модель в файл
        with open(output_path, 'wb') as f:
            pickle.dump(model, f)
            
        print(f"Модель успешно сохранена в {output_path}")
        
    except Exception as e:
        print(f"Ошибка при загрузке модели: {e}")

if __name__ == "__main__":
    RUN_ID = "4a08cd3868eb463baaee2dcbf614a72c" 
    # Загружаем модель
    download_model(RUN_ID)