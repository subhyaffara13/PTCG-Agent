from typing import Any, Optional

def hf_chat_template(model: str, messages: list, chat_template: Optional[Any] = None):
    """HuggingFace chat template (sync version)"""
    from litellm.litellm_core_utils.prompt_templates.huggingface_template_handler import (
        _get_chat_template_file,
        _get_tokenizer_config,
        strftime_now,
    )

    env = ImmutableSandboxedEnvironment()
    env.globals["raise_exception"] = lambda msg: Exception(f"Error message - {msg}")
    env.globals["strftime_now"] = strftime_now

    template, bos_token, eos_token = _fetch_and_extract_template(
        model=model,
        chat_template=chat_template,
        get_config_fn=_get_tokenizer_config,
        get_template_fn=_get_chat_template_file,
    )
    return _render_chat_template(
        env=env,
        chat_template=template,
        bos_token=bos_token,
        eos_token=eos_token,
        messages=messages,
    )

