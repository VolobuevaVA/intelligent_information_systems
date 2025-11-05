cd /home/mainuser/intelligent_information_systems/mlflow
mlflow server --backend-store-uri sqlite:///mlruns.db --default-artifact-root ./mlartifacts --host 0.0.0.0 --port 5000
