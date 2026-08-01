
def _check_prisma_client():
    """Helper to check if prisma_client is available and raise appropriate error"""
    from litellm.proxy.proxy_server import prisma_client

    if prisma_client is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Database not initialized"},
        )
    return prisma_client

