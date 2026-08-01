
def decrypt_env_var() -> Dict[str, Any]:
    # setup client class
    aws_kms = AWSKeyManagementService_V2()
    # iterate through env - for `aws_kms/`
    new_values = {}
    for k, v in os.environ.items():
        if (
            k is not None
            and isinstance(k, str)
            and k.lower().startswith("litellm_secret_aws_kms")
        ) or (v is not None and isinstance(v, str) and v.startswith("aws_kms/")):
            decrypted_value = aws_kms.decrypt_value(secret_name=k)
            # reset env var
            k = re.sub("litellm_secret_aws_kms_", "", k, flags=re.IGNORECASE)
            new_values[k] = decrypted_value

    return new_values

