
def define_sagemaker_information():
    try:
        instance_data = httpx.get(os.environ["ECS_CONTAINER_METADATA_URI"]).json()
        dlc_container_used = instance_data["Image"]
        dlc_tag = instance_data["Image"].split(":")[1]
    except Exception:
        dlc_container_used = None
        dlc_tag = None

    sagemaker_params = json.loads(os.getenv("SM_FRAMEWORK_PARAMS", "{}"))
    runs_distributed_training = "sagemaker_distributed_dataparallel_enabled" in sagemaker_params
    training_job_arn = os.getenv("TRAINING_JOB_ARN")
    account_id = training_job_arn.split(":")[4] if training_job_arn is not None else None

    sagemaker_object = {
        "sm_framework": os.getenv("SM_FRAMEWORK_MODULE", None),
        "sm_region": os.getenv("AWS_REGION", None),
        "sm_number_gpu": os.getenv("SM_NUM_GPUS", "0"),
        "sm_number_cpu": os.getenv("SM_NUM_CPUS", "0"),
        "sm_distributed_training": runs_distributed_training,
        "sm_deep_learning_container": dlc_container_used,
        "sm_deep_learning_container_tag": dlc_tag,
        "sm_account_id": account_id,
    }
    return sagemaker_object

