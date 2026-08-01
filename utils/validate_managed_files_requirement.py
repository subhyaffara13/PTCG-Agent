
def validate_managed_files_requirement(
    target_model_names: List[str],
    model: Optional[str] = None,
) -> None:
    """
    Enforce proxy-level managed files when litellm.require_managed_files is enabled.

    Raises:
        HTTPException: 400 if the upload would bypass the managed-files flow, i.e.
            target_model_names is missing or a model parameter routes the request
            through the direct provider path instead of the managed-files hook.
    """
    import litellm
    from fastapi import HTTPException

    if litellm.require_managed_files is not True:
        return

    if not target_model_names:
        raise HTTPException(
            status_code=400,
            detail=(
                "target_model_names is required when require_managed_files is enabled "
                "in litellm_settings. Provide one or more model aliases via the "
                "target_model_names form field (e.g. target_model_names=my-model-alias)."
            ),
        )

    if model:
        raise HTTPException(
            status_code=400,
            detail=(
                "model is not allowed when require_managed_files is enabled in "
                "litellm_settings. Uploads must go through managed files using "
                "target_model_names instead of the model parameter."
            ),
        )

