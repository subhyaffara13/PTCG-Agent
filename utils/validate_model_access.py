
def validate_model_access(
    model_id: str,
    available_models: List[str],
) -> None:
    """
    Validate that a model is accessible to the user.
    Supports batch requests with comma-separated model IDs.

    Args:
        model_id: The model ID to validate (can be comma-separated for batch requests)
        available_models: List of models available to the user

    Raises:
        HTTPException: If the model is not accessible
    """
    # Handle batch requests with comma-separated models
    if "," in model_id:
        models = [m.strip() for m in model_id.split(",")]
        inaccessible_models = [m for m in models if m not in available_models]
        if inaccessible_models:
            raise HTTPException(
                status_code=404,
                detail="The following model(s) do not exist or are not accessible: {}".format(
                    ", ".join(inaccessible_models)
                ),
            )
    else:
        # Single model validation
        if model_id not in available_models:
            raise HTTPException(
                status_code=404,
                detail="The model `{}` does not exist or is not accessible".format(
                    model_id
                ),
            )

