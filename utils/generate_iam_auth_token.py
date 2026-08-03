import os
from typing import Any, Optional

def generate_iam_auth_token(
    db_host, db_port, db_user, client: Optional[Any] = None
) -> str:
    from urllib.parse import quote

    if client is None:
        boto_client = init_rds_client(
            aws_region_name=os.getenv("AWS_REGION_NAME"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_session_name=os.getenv("AWS_SESSION_NAME"),
            aws_profile_name=os.getenv("AWS_PROFILE_NAME"),
            aws_role_name=os.getenv("AWS_ROLE_NAME", os.getenv("AWS_ROLE_ARN")),
            aws_web_identity_token=os.getenv(
                "AWS_WEB_IDENTITY_TOKEN", os.getenv("AWS_WEB_IDENTITY_TOKEN_FILE")
            ),
        )
    else:
        boto_client = client

    token = boto_client.generate_db_auth_token(
        DBHostname=db_host, Port=db_port, DBUsername=db_user
    )
    cleaned_token = quote(token, safe="")

    return cleaned_token

