
def get_service_account_rab_endpoint(service_account_email: str) -> str:
    """Builds the Regional Access Boundary lookup URL for service accounts.

    Args:
        service_account_email: The service account email.

    Returns:
        str: The complete lookup URL.
    """
    return f"https://{_get_domain()}/v1/projects/-/serviceAccounts/{service_account_email}/allowedLocations"

