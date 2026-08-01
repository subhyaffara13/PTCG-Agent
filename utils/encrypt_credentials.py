
def encrypt_credentials(
    credentials: MCPCredentials, encryption_key: Optional[str]
) -> MCPCredentials:
    auth_value = credentials.get("auth_value")
    if auth_value is not None:
        credentials["auth_value"] = encrypt_value_helper(
            value=auth_value,
            new_encryption_key=encryption_key,
        )
    client_id = credentials.get("client_id")
    if client_id is not None:
        credentials["client_id"] = encrypt_value_helper(
            value=client_id,
            new_encryption_key=encryption_key,
        )
    client_secret = credentials.get("client_secret")
    if client_secret is not None:
        credentials["client_secret"] = encrypt_value_helper(
            value=client_secret,
            new_encryption_key=encryption_key,
        )
    # AWS SigV4 credential fields
    aws_access_key_id = credentials.get("aws_access_key_id")
    if aws_access_key_id is not None:
        credentials["aws_access_key_id"] = encrypt_value_helper(
            value=aws_access_key_id,
            new_encryption_key=encryption_key,
        )
    aws_secret_access_key = credentials.get("aws_secret_access_key")
    if aws_secret_access_key is not None:
        credentials["aws_secret_access_key"] = encrypt_value_helper(
            value=aws_secret_access_key,
            new_encryption_key=encryption_key,
        )
    aws_session_token = credentials.get("aws_session_token")
    if aws_session_token is not None:
        credentials["aws_session_token"] = encrypt_value_helper(
            value=aws_session_token,
            new_encryption_key=encryption_key,
        )
    # aws_region_name and aws_service_name are NOT secrets — stored as-is
    return credentials

