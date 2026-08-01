
def _fetch_and_extract_template(
    model: str, chat_template: Optional[Any], get_config_fn, get_template_fn
) -> Tuple[str, str, str]:
    """
    Sync version: Fetch template and tokens from HuggingFace.

    Returns: (chat_template, bos_token, eos_token)
    """
    from litellm.litellm_core_utils.prompt_templates.huggingface_template_handler import (
        _extract_token_value,
    )

    bos_token = ""
    eos_token = ""

    if chat_template is None:
        # Fetch or retrieve cached tokenizer config
        if model in litellm.known_tokenizer_config:
            tokenizer_config = litellm.known_tokenizer_config[model]
        else:
            tokenizer_config = get_config_fn(hf_model_name=model)
            litellm.known_tokenizer_config.update({model: tokenizer_config})

        # Try to get chat template from tokenizer_config.json first
        if (
            tokenizer_config.get("status") == "success"
            and "tokenizer" in tokenizer_config
            and isinstance(tokenizer_config["tokenizer"], dict)
            and "chat_template" in tokenizer_config["tokenizer"]
        ):
            tokenizer_data: dict = tokenizer_config["tokenizer"]  # type: ignore
            bos_token = _extract_token_value(
                token_value=tokenizer_data.get("bos_token")
            )
            eos_token = _extract_token_value(
                token_value=tokenizer_data.get("eos_token")
            )
            chat_template = tokenizer_data["chat_template"]
        else:
            # Fallback: Try to fetch chat template from separate .jinja file
            template_result = get_template_fn(hf_model_name=model)
            if template_result.get("status") == "success":
                chat_template = template_result["chat_template"]
                # Still try to get tokens from tokenizer_config if available
                if (
                    tokenizer_config.get("status") == "success"
                    and "tokenizer" in tokenizer_config
                    and isinstance(tokenizer_config["tokenizer"], dict)
                ):
                    tokenizer_data: dict = tokenizer_config["tokenizer"]  # type: ignore
                    bos_token = _extract_token_value(
                        token_value=tokenizer_data.get("bos_token")
                    )
                    eos_token = _extract_token_value(
                        token_value=tokenizer_data.get("eos_token")
                    )
            else:
                raise Exception("No chat template found")

    return chat_template, bos_token, eos_token  # type: ignore

