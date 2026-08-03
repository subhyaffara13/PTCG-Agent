from typing import Dict, List

def _convert_watsonx_messages_core(
    model: str,
    messages: List[AllMessageValues],
    provider: str,
    custom_prompt_dict: Dict,
    apply_template_fn,
) -> str:
    """Sync core logic for converting watsonx messages to prompt"""
    from litellm.types.llms.watsonx import WatsonXModelPattern

    # handle anthropic prompts and amazon titan prompts
    if model in custom_prompt_dict:
        model_prompt_dict = custom_prompt_dict[model]
        return ptf.custom_prompt(
            messages=messages,
            role_dict=model_prompt_dict.get(
                "role_dict", model_prompt_dict.get("roles")
            ),
            initial_prompt_value=model_prompt_dict.get("initial_prompt_value", ""),
            final_prompt_value=model_prompt_dict.get("final_prompt_value", ""),
            bos_token=model_prompt_dict.get("bos_token", ""),
            eos_token=model_prompt_dict.get("eos_token", ""),
        )
    elif provider == WatsonXModelPattern.IBM_MISTRALAI.value:
        return ptf.mistral_instruct_pt(messages=messages)
    else:
        # Try applying specific template first
        result = apply_template_fn(model=model, messages=messages)
        if result:
            return result
        # Fallback to default
        return ptf.prompt_factory(
            model=model, messages=messages, custom_llm_provider="watsonx"
        )  # type: ignore

