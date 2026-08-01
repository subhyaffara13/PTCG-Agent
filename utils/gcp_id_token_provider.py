
def gcp_id_token_provider(
    audience: str = "https://api.openai.com/v1",
    *,
    timeout: float = 10.0,
    http_client: httpx.Client | None = None,
) -> SubjectTokenProvider:
    """
    Get a subject token provider for GCP VM instances using the instance metadata server.

    See: https://cloud.google.com/compute/docs/instances/verifying-instance-identity

    Args:
        audience: the unique URI agreed upon by both the instance and the system verifying
            the instance's identity. Defaults to `https://api.openai.com/v1`.
        timeout: the request timeout in seconds. Defaults to 10.0.
        http_client: optional httpx.Client instance to use for requests. If not provided, a new client will be created for each request.
    """

    def get_token() -> str:
        try:
            url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity"
            params = {"audience": audience}

            if http_client is not None:
                response = http_client.get(url, params=params, headers={"Metadata-Flavor": "Google"}, timeout=timeout)
            else:
                with httpx.Client() as client:
                    response = client.get(url, params=params, headers={"Metadata-Flavor": "Google"}, timeout=timeout)

            if response.is_error:
                raise SubjectTokenProviderError(
                    f"Failed to fetch GCP subject token from metadata server: HTTP {response.status_code}",
                    response=response,
                )
            token = response.text.strip()
            if not token:
                raise SubjectTokenProviderError("GCP metadata server returned an empty token", response=response)
            return token
        except Exception as e:
            raise SubjectTokenProviderError(f"Failed to fetch GCP subject token from metadata server: {e}") from e

    return {"token_type": "id", "get_token": get_token}

