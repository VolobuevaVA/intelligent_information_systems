def predict(self, features: List[float]) -> float:
    """
    Предсказание для одного объекта
    """
    if self.model is None:
        logger.error("Модель не загружена")
        return 0.0
    
    try:
        logger.info(f"Получены фичи: {features}")
        logger.info(f"Количество фич: {len(features)}")
        
        # Проверяем количество фич
        if len(features) != 7:
            logger.error(f"Ожидается 7 фич, получено {len(features)}")
            # Можно вернуть ошибку или дополнить нулями
            # Пока вернем 0 для простоты
            return 0.0
        
        # Преобразуем признаки в DataFrame
        features_df = pd.DataFrame([features])
        
        # Делаем предсказание
        prediction = self.model.predict(features_df)
        
        # Извлекаем значение
        if hasattr(prediction, '__len__') and len(prediction) > 0:
            result = float(prediction[0])
        else:
            result = float(prediction)
            
        logger.info(f"Final prediction: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Ошибка при предсказании: {e}")
        return 0.0