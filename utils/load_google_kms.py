
def load_google_kms(use_google_kms: Optional[bool]):
    if use_google_kms is None or use_google_kms is False:
        return
    try:
        from google.cloud import kms_v1  # type: ignore

        validate_environment()

        # Create the KMS client
        client = kms_v1.KeyManagementServiceClient()
        litellm.secret_manager_client = client
        litellm._key_management_system = KeyManagementSystem.GOOGLE_KMS
        litellm._google_kms_resource_name = os.getenv("GOOGLE_KMS_RESOURCE_NAME")
    except Exception as e:
        raise e

