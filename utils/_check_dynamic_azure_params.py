
def _check_dynamic_azure_params(
    azure_client_params: dict,
    azure_client: Optional[Union[AzureOpenAI, AsyncAzureOpenAI]],
) -> bool:
    """
    Returns True if user passed in client params != initialized azure client

    Currently only implemented for api version
    """
    if azure_client is None:
        return True

    dynamic_params = ["api_version"]
    for k, v in azure_client_params.items():
        if k in dynamic_params and k == "api_version":
            if v is not None and v != azure_client._custom_query["api-version"]:
                return True

    return False

