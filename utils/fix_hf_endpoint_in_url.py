
def fix_hf_endpoint_in_url(url: str, endpoint: str | None) -> str:
    """Replace the default endpoint in a URL by a custom one.

    This is useful when using a proxy and the Hugging Face Hub returns a URL with the default endpoint.
    """
    endpoint = endpoint.rstrip("/") if endpoint else constants.ENDPOINT
    # check if a proxy has been set => if yes, update the returned URL to use the proxy
    if endpoint not in (constants._HF_DEFAULT_ENDPOINT, constants._HF_DEFAULT_STAGING_ENDPOINT):
        url = url.replace(constants._HF_DEFAULT_ENDPOINT, endpoint)
        url = url.replace(constants._HF_DEFAULT_STAGING_ENDPOINT, endpoint)
    return url

