
def _extract_response_obj_and_hidden_params(
    init_response_obj: Union[Any, BaseModel, dict],
    original_exception: Optional[Exception],
) -> Tuple[dict, Optional[dict]]:
    """Extract response_obj and hidden_params from init_response_obj."""
    hidden_params: Optional[dict] = None
    if init_response_obj is None:
        response_obj = {}
    elif isinstance(init_response_obj, BaseModel):
        response_obj = init_response_obj.model_dump()
        hidden_params = getattr(init_response_obj, "_hidden_params", None)
    elif isinstance(init_response_obj, dict):
        response_obj = init_response_obj
    else:
        response_obj = {}

    if original_exception is not None and hidden_params is None:
        response_headers = _get_response_headers(original_exception)
        if response_headers is not None:
            hidden_params = dict(
                StandardLoggingHiddenParams(
                    additional_headers=StandardLoggingPayloadSetup.get_additional_headers(
                        dict(response_headers)
                    ),
                    model_id=None,
                    cache_key=None,
                    api_base=None,
                    response_cost=None,
                    litellm_overhead_time_ms=None,
                    batch_models=None,
                    litellm_model_name=None,
                    usage_object=None,
                )
            )

    return response_obj, hidden_params

