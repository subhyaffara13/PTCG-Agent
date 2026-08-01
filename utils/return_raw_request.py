
def return_raw_request(endpoint: CallTypes, kwargs: dict) -> RawRequestTypedDict:
    """
    Return the json str of the request

    This is currently in BETA, and tested for `/chat/completions` -> `litellm.completion` calls.
    """
    from datetime import datetime

    from litellm.litellm_core_utils.litellm_logging import Logging

    litellm_logging_obj = Logging(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "hi"}],
        stream=False,
        call_type="acompletion",
        litellm_call_id="1234",
        start_time=datetime.now(),
        function_id="1234",
        log_raw_request_response=True,
    )

    llm_api_endpoint = getattr(litellm, endpoint.value)

    received_exception = ""

    try:
        llm_api_endpoint(
            **kwargs,
            litellm_logging_obj=litellm_logging_obj,
            api_key="my-fake-api-key",  # 👈 ensure the request fails
        )
    except Exception as e:
        received_exception = str(e)

    raw_request_typed_dict = litellm_logging_obj.model_call_details.get(
        "raw_request_typed_dict"
    )
    if raw_request_typed_dict:
        return cast(RawRequestTypedDict, raw_request_typed_dict)
    else:
        return RawRequestTypedDict(
            error=received_exception,
        )

