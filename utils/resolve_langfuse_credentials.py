import os

def resolve_langfuse_credentials(
    langfuse_public_key=None,
    langfuse_secret=None,
    langfuse_secret_key=None,
    langfuse_host=None,
    allow_env_credentials: bool = True,
):
    if allow_env_credentials is False and langfuse_host is not None:
        secret_key = langfuse_secret or langfuse_secret_key
        public_key = langfuse_public_key
    else:
        secret_key = (
            langfuse_secret or langfuse_secret_key or os.getenv("LANGFUSE_SECRET_KEY")
        )
        public_key = langfuse_public_key or os.getenv("LANGFUSE_PUBLIC_KEY")

    resolved_host = langfuse_host or os.getenv(
        "LANGFUSE_HOST", "https://cloud.langfuse.com"
    )

    return public_key, secret_key, resolved_host

