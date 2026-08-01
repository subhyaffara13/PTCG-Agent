
def _has_azure_ad_credentials() -> bool:
    return (
        _os.environ.get("AZURE_OPENAI_AD_TOKEN") is not None
        or azure_ad_token is not None
        or azure_ad_token_provider is not None
    )

