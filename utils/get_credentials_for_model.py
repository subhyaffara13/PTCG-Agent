
def get_credentials_for_model(
    llm_router,  # Router instance
    model_id: str,
    operation_context: str = "file operation",
):
    """
    Retrieve API credentials for a model from the LLM Router.

    Args:
        llm_router: LiteLLM Router instance
        model_id: Model name or deployment ID
        operation_context: Description for error messages (e.g., "file upload", "batch creation")

    Returns:
        Dictionary with credentials (api_key, api_base, custom_llm_provider, etc.)

    Raises:
        HTTPException: If router not initialized or model not found
    """
    from fastapi import HTTPException

    if llm_router is None:
        raise HTTPException(
            status_code=500,
            detail={"error": "Router not initialized. Cannot use model-based routing."},
        )

    credentials = llm_router.get_deployment_credentials_with_provider(model_id=model_id)

    if credentials is None:
        raise HTTPException(
            status_code=400,
            detail={
                "error": f"Model '{model_id}' not found in model_list. Please check your config.yaml."
            },
        )

    return credentials

