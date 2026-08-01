
def register_prompt_template(
    model: str,
    roles: dict = {},
    initial_prompt_value: str = "",
    final_prompt_value: str = "",
    tokenizer_config: dict = {},
):
    """
    Register a prompt template to follow your custom format for a given model

    Args:
        model (str): The name of the model.
        roles (dict): A dictionary mapping roles to their respective prompt values.
        initial_prompt_value (str, optional): The initial prompt value. Defaults to "".
        final_prompt_value (str, optional): The final prompt value. Defaults to "".

    Returns:
        dict: The updated custom prompt dictionary.
    Example usage:
    ```
    import litellm
    litellm.register_prompt_template(
            model="llama-2",
        initial_prompt_value="You are a good assistant" # [OPTIONAL]
            roles={
            "system": {
                "pre_message": "[INST] <<SYS>>\n", # [OPTIONAL]
                "post_message": "\n<</SYS>>\n [/INST]\n" # [OPTIONAL]
            },
            "user": {
                "pre_message": "[INST] ", # [OPTIONAL]
                "post_message": " [/INST]" # [OPTIONAL]
            },
            "assistant": {
                "pre_message": "\n" # [OPTIONAL]
                "post_message": "\n" # [OPTIONAL]
            }
        }
        final_prompt_value="Now answer as best you can:" # [OPTIONAL]
    )
    ```
    """
    complete_model = model
    potential_models = [complete_model]
    try:
        get_llm_provider = getattr(sys.modules[__name__], "get_llm_provider")
        model = get_llm_provider(model=model)[0]
        potential_models.append(model)
    except Exception:
        pass
    if tokenizer_config:
        for m in potential_models:
            litellm.known_tokenizer_config[m] = {
                "tokenizer": tokenizer_config,
                "status": "success",
            }
    else:
        for m in potential_models:
            litellm.custom_prompt_dict[m] = {
                "roles": roles,
                "initial_prompt_value": initial_prompt_value,
                "final_prompt_value": final_prompt_value,
            }

    return litellm.custom_prompt_dict

