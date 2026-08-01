
def response_schema_prompt(model: str, response_schema: dict) -> str:
    """
    Decides if a user-defined custom prompt or default needs to be used

    Returns the prompt str that's passed to the model as a user message
    """
    custom_prompt_details: Optional[dict] = None
    response_schema_as_message = [
        {"role": "user", "content": "{}".format(response_schema)}
    ]
    if f"{model}/response_schema_prompt" in litellm.custom_prompt_dict:
        custom_prompt_details = litellm.custom_prompt_dict[
            f"{model}/response_schema_prompt"
        ]  # allow user to define custom response schema prompt by model
    elif "response_schema_prompt" in litellm.custom_prompt_dict:
        custom_prompt_details = litellm.custom_prompt_dict["response_schema_prompt"]

    if custom_prompt_details is not None:
        return custom_prompt(
            role_dict=custom_prompt_details["roles"],
            initial_prompt_value=custom_prompt_details["initial_prompt_value"],
            final_prompt_value=custom_prompt_details["final_prompt_value"],
            messages=response_schema_as_message,
        )
    else:
        return default_response_schema_prompt(response_schema=response_schema)

