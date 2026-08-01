
def _get_api_params(params: dict, model: Optional[str] = None) -> WatsonXAPIParams:
    """
    Find watsonx.ai credentials in the params or environment variables and return the headers for authentication.
    """
    # Load auth variables from params
    project_id = params.pop(
        "project_id", params.pop("watsonx_project", None)
    )  # watsonx.ai project_id - allow 'watsonx_project' to be consistent with how vertex project implementation works -> reduce provider-specific params
    space_id = params.pop("space_id", None)  # watsonx.ai deployment space_id
    region_name = params.pop("region_name", params.pop("region", None))
    if region_name is None:
        region_name = params.pop(
            "watsonx_region_name", params.pop("watsonx_region", None)
        )  # consistent with how vertex ai + aws regions are accepted

    # Load auth variables from environment variables
    if project_id is None:
        project_id = (
            get_secret_str("WATSONX_PROJECT_ID")
            or get_secret_str("WX_PROJECT_ID")
            or get_secret_str("PROJECT_ID")
        )
    if region_name is None:
        region_name = (
            get_secret_str("WATSONX_REGION")
            or get_secret_str("WX_REGION")
            or get_secret_str("REGION")
        )
    if space_id is None:
        space_id = (
            get_secret_str("WATSONX_DEPLOYMENT_SPACE_ID")
            or get_secret_str("WATSONX_SPACE_ID")
            or get_secret_str("WX_SPACE_ID")
            or get_secret_str("SPACE_ID")
        )

    if (
        project_id is None
        and space_id is None
        and model is not None
        and not model.startswith("deployment/")
    ):
        raise WatsonXAIError(
            status_code=401,
            message="Error: Watsonx project_id and space_id not set. Set WX_PROJECT_ID or WX_SPACE_ID in environment variables or pass in as a parameter.",
        )

    return WatsonXAPIParams(
        project_id=project_id,
        space_id=space_id,
        region_name=region_name,
    )

