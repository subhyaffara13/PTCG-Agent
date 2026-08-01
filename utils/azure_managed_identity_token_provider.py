
def azure_managed_identity_token_provider(
    resource: str = "https://management.azure.com/",
    *,
    object_id: str | None = None,
    client_id: str | None = None,
    msi_res_id: str | None = None,
    api_version: str = "2018-02-01",
    timeout: float = 10.0,
    http_client: httpx.Client | None = None,
) -> SubjectTokenProvider:
    """
    Get a subject token provider for Azure Managed Identities.

    See: https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-use-vm-token#get-a-token-using-http

    Args:
        resource: the resource URI to request a token for. Defaults to `https://management.azure.com/` (Azure Resource Manager).
        object_id: the object ID of the managed identity to use, when multiple are assigned.
        client_id: the client ID of the managed identity to use, when multiple are assigned.
        msi_res_id: the ARM resource ID of the managed identity to use, when multiple are assigned.
        api_version: the Azure IMDS API version. Defaults to `2018-02-01`.
        timeout: the request timeout in seconds. Defaults to 10.0.
        http_client: optional httpx.Client instance to use for requests. If not provided, a new client will be created for each request.
    """

    def get_token() -> str:
        try:
            url = "http://169.254.169.254/metadata/identity/oauth2/token"
            params: dict[str, str] = {"api-version": api_version, "resource": resource}
            if object_id is not None:
                params["object_id"] = object_id
            if client_id is not None:
                params["client_id"] = client_id
            if msi_res_id is not None:
                params["msi_res_id"] = msi_res_id

            if http_client is not None:
                response = http_client.get(url, params=params, headers={"Metadata": "true"}, timeout=timeout)
            else:
                with httpx.Client() as client:
                    response = client.get(url, params=params, headers={"Metadata": "true"}, timeout=timeout)

            if response.is_error:
                raise SubjectTokenProviderError(
                    f"Failed to fetch Azure subject token from IMDS: HTTP {response.status_code}",
                    response=response,
                )
            data = response.json()
            token = data.get("access_token")
            if not token:
                raise SubjectTokenProviderError(
                    "Azure IMDS response did not include an access_token", response=response
                )
            return cast(str, token)
        except Exception as e:
            raise SubjectTokenProviderError(f"Failed to fetch Azure subject token from IMDS: {e}") from e

    return {"token_type": "jwt", "get_token": get_token}

