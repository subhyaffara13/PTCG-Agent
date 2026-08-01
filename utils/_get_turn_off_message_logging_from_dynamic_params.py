
def _get_turn_off_message_logging_from_dynamic_params(
    model_call_details: dict,
) -> Optional[bool]:
    """
    gets the value of `turn_off_message_logging` from the dynamic params, if it exists.

    handles boolean and string values of `turn_off_message_logging`
    """
    standard_callback_dynamic_params: Optional[StandardCallbackDynamicParams] = (
        model_call_details.get("standard_callback_dynamic_params", None)
    )
    if standard_callback_dynamic_params:
        _turn_off_message_logging = standard_callback_dynamic_params.get(
            "turn_off_message_logging"
        )
        if isinstance(_turn_off_message_logging, bool):
            return _turn_off_message_logging
        elif isinstance(_turn_off_message_logging, str):
            return str_to_bool(_turn_off_message_logging)
    return None

