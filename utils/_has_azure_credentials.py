
def _has_azure_credentials() -> bool:
    return azure_endpoint is not None or _os.environ.get("AZURE_OPENAI_API_KEY") is not None

