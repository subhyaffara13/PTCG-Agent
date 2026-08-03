from typing import Optional

def _get_langfuse_proxy_credentials(
    *,
    dynamic_host_supplied: bool,
    dynamic_langfuse_public_key: Optional[str],
    dynamic_langfuse_secret_key: Optional[str],
):
    if dynamic_host_supplied:
        if not dynamic_langfuse_public_key or not dynamic_langfuse_secret_key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Dynamic Langfuse hosts must include dynamic Langfuse credentials"
                },
            )
        return dynamic_langfuse_public_key, dynamic_langfuse_secret_key

    return (
        dynamic_langfuse_public_key
        or litellm.utils.get_secret(secret_name="LANGFUSE_PUBLIC_KEY"),
        dynamic_langfuse_secret_key
        or litellm.utils.get_secret(secret_name="LANGFUSE_SECRET_KEY"),
    )

