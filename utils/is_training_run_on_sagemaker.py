
def is_training_run_on_sagemaker() -> bool:
    return "SAGEMAKER_JOB_NAME" in os.environ

