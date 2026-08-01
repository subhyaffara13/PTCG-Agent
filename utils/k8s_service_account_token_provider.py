
def k8s_service_account_token_provider(
    token_file_path: str | Path = "/var/run/secrets/kubernetes.io/serviceaccount/token",
) -> SubjectTokenProvider:
    """
    Get a subject token provider for Kubernetes clusters with Workload Identity configured.

    Cloud providers typically mount the subject token as a file in the container.

    Args:
        token_file_path: path to the mounted service account token file. Defaults to `/var/run/secrets/kubernetes.io/serviceaccount/token`.
    """

    def get_token() -> str:
        try:
            with open(token_file_path, "r") as f:
                token = f.read().strip()
                if not token:
                    raise SubjectTokenProviderError(f"The token file at {token_file_path} is empty.")
                return token
        except Exception as e:
            raise SubjectTokenProviderError(f"Failed to read the token file at {token_file_path}: {e}") from e

    return {"token_type": "jwt", "get_token": get_token}

