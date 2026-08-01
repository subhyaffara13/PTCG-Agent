
def get_workload_identity_pool_rab_endpoint(project_number: str, pool_id: str) -> str:
    """Builds the Regional Access Boundary lookup URL for workload identity pools.

    Args:
        project_number: The Google Cloud project number.
        pool_id: The workload identity pool ID.

    Returns:
        str: The complete lookup URL.
    """
    return f"https://{_get_domain()}/v1/projects/{project_number}/locations/global/workloadIdentityPools/{pool_id}/allowedLocations"

