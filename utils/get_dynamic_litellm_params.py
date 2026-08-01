
def get_dynamic_litellm_params(litellm_params: dict, request_kwargs: dict) -> dict:
    """
    Generate a unique model_id for the deployment.

    Returns
    - litellm_params: dict

    for generating a unique model_id.
    """
    # update litellm_params with clientside credentials
    for key in clientside_credential_keys:
        if key in request_kwargs:
            litellm_params[key] = request_kwargs[key]

    # If the caller redirected api_base/base_url to a client-controlled value,
    # don't forward the admin's organization / extra_body / region / token /
    # vertex / aws fields — those were meant for the original upstream.
    # Always drop the admin's value first, then write the caller's value back
    # if they resupplied the field. The naive
    # ``if field not in request_kwargs: pop`` shape lets a caller *echo* a
    # field name (with any value, including an empty string) to keep the
    # admin's value in ``litellm_params`` and have it forwarded to the
    # redirected upstream.
    if "api_base" in request_kwargs or "base_url" in request_kwargs:
        for field in _ADMIN_CONFIG_FIELDS_TO_CLEAR_ON_BASE_OVERRIDE:
            litellm_params.pop(field, None)
            if field in request_kwargs:
                litellm_params[field] = request_kwargs[field]

    return litellm_params

