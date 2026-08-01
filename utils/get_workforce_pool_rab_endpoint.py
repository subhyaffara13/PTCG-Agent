
def get_workforce_pool_rab_endpoint(pool_id: str) -> str:
    """Builds the Regional Access Boundary lookup URL for workforce pools.

    Args:
        pool_id: The workforce pool ID.

    Returns:
        str: The complete lookup URL.
    """
    return f"https://{_get_domain()}/v1/locations/global/workforcePools/{pool_id}/allowedLocations"

