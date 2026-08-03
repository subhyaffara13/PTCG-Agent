from typing import Optional

def _health_endpoint_resolve_target_model_name(
    model: Optional[str],
    model_id: Optional[str],
    llm_router,
) -> Optional[str]:
    """Map ``model_id`` (without ``model``) to ``model_name`` for live health checks."""
    if not model_id or model:
        return model
    if llm_router is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Model with ID {model_id} not found"},
        )
    try:
        deployment = llm_router.get_deployment(model_id=model_id)
    except Exception as e:
        verbose_proxy_logger.error(
            f"Error getting deployment for model_id {model_id}: {e}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Model with ID {model_id} not found"},
        ) from e
    if deployment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Model with ID {model_id} not found"},
        )
    return deployment.model_name

