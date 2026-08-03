import os

def langfuse_client_init(
    langfuse_public_key=None,
    langfuse_secret=None,
    langfuse_secret_key=None,
    langfuse_host=None,
    flush_interval=1,
    allow_env_credentials: bool = True,
) -> LangfuseClass:
    """
    Initialize Langfuse client with caching to prevent multiple initializations.

    Args:
        langfuse_public_key (str, optional): Public key for Langfuse. Defaults to None.
        langfuse_secret (str, optional): Secret key for Langfuse. Defaults to None.
        langfuse_host (str, optional): Host URL for Langfuse. Defaults to None.
        flush_interval (int, optional): Flush interval in seconds. Defaults to 1.

    Returns:
        Langfuse: Initialized Langfuse client instance

    Raises:
        Exception: If langfuse package is not installed
    """
    try:
        import langfuse
        from langfuse import Langfuse
    except Exception as e:
        raise Exception(
            f"\033[91mLangfuse not installed, try running 'pip install langfuse' to fix this error: {e}\n\033[0m"
        )

    public_key, secret_key, langfuse_host = resolve_langfuse_credentials(
        langfuse_public_key=langfuse_public_key,
        langfuse_secret=langfuse_secret,
        langfuse_secret_key=langfuse_secret_key,
        langfuse_host=langfuse_host,
        allow_env_credentials=allow_env_credentials,
    )

    if not (
        langfuse_host.startswith("http://") or langfuse_host.startswith("https://")
    ):
        # add http:// if unset, assume communicating over private network - e.g. render
        langfuse_host = "http://" + langfuse_host

    langfuse_release = os.getenv("LANGFUSE_RELEASE")
    langfuse_debug = os.getenv("LANGFUSE_DEBUG")

    parameters = {
        "public_key": public_key,
        "secret_key": secret_key,
        "host": langfuse_host,
        "release": langfuse_release,
        "debug": langfuse_debug,
        "flush_interval": LangFuseLogger._get_langfuse_flush_interval(
            flush_interval
        ),  # flush interval in seconds
    }

    if Version(langfuse.version.__version__) >= Version("2.6.0"):
        parameters["sdk_integration"] = "litellm"

    if Version(langfuse.version.__version__) >= Version("2.7.3"):
        import httpx

        import litellm

        from ...llms.custom_httpx.http_handler import get_ssl_configuration

        parameters["httpx_client"] = httpx.Client(
            verify=get_ssl_configuration(),
            cert=os.getenv("SSL_CERTIFICATE", litellm.ssl_certificate),
        )

    client = Langfuse(**parameters)

    return client

