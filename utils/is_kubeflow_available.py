import os

def is_kubeflow_available():
    if os.getenv("DISABLE_KUBEFLOW_INTEGRATION", "FALSE").upper() == "TRUE":
        return False
    return os.getenv("KUBEFLOW_TRAINER_SERVER_URL") is not None

