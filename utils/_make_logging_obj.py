from typing import Any, Dict, Optional

def _make_logging_obj(
    kwargs: Dict[str, Any],
    model: str,
    custom_llm_provider: str,
    call_type: str,
    optional_params: Dict[str, Any],
) -> LiteLLMLoggingObj:
    litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
    litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
    litellm_logging_obj.update_from_kwargs(
        kwargs=kwargs,
        model=model,
        optional_params=optional_params,
        litellm_params={"litellm_call_id": litellm_call_id},
        custom_llm_provider=custom_llm_provider,
    )
    return litellm_logging_obj

