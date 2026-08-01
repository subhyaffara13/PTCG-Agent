
def convert_watsonx_messages_to_prompt(
    model: str,
    messages: List[AllMessageValues],
    provider: str,
    custom_prompt_dict: Dict,
) -> str:
    """Sync version of convert_watsonx_messages_to_prompt"""
    from litellm.llms.watsonx.chat.transformation import IBMWatsonXChatConfig

    return _convert_watsonx_messages_core(
        model=model,
        messages=messages,
        provider=provider,
        custom_prompt_dict=custom_prompt_dict,
        apply_template_fn=IBMWatsonXChatConfig.apply_prompt_template,
    )

