
def _generate_gcp_iam_access_token(service_account: str) -> str:
    """
    Generate GCP IAM access token for Redis authentication.

    Args:
        service_account: GCP service account in format 'projects/-/serviceAccounts/name@project.iam.gserviceaccount.com'

    Returns:
        Access token string for GCP IAM authentication
    """
    try:
        from google.cloud import iam_credentials_v1
    except ImportError:
        raise ImportError(
            "google-cloud-iam is required for GCP IAM Redis authentication. "
            "Install it with: pip install google-cloud-iam"
        )

    client = iam_credentials_v1.IAMCredentialsClient()
    request = iam_credentials_v1.GenerateAccessTokenRequest(
        name=service_account,
        scope=["https://www.googleapis.com/auth/cloud-platform"],
    )
    response = client.generate_access_token(request=request)
    return str(response.access_token)

