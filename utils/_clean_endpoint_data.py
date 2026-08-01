
def _clean_endpoint_data(endpoint_data: dict, details: Optional[bool] = True):
    """
    Clean the endpoint data for display to users.
    """
    endpoint_data.pop("litellm_logging_obj", None)
    return (
        {k: v for k, v in endpoint_data.items() if k not in ILLEGAL_DISPLAY_PARAMS}
        if details is not False
        else {k: v for k, v in endpoint_data.items() if k in MINIMAL_DISPLAY_PARAMS}
    )

