import sys
from typing import List, Optional

def add_provider_specific_params_to_optional_params(
    optional_params: dict,
    passed_params: dict,
    custom_llm_provider: str,
    openai_params: List[str],
    additional_drop_params: Optional[list] = None,
) -> dict:
    """
    Add provider specific params to optional_params
    """

    if (
        custom_llm_provider
        in ["openai", "azure", "text-completion-openai"]
        + litellm.openai_compatible_providers
    ):
        # for openai, azure we should pass the extra/passed params within `extra_body` https://github.com/openai/openai-python/blob/ac33853ba10d13ac149b1fa3ca6dba7d613065c9/src/openai/resources/models.py#L46
        if (
            _should_drop_param(
                k="extra_body", additional_drop_params=additional_drop_params
            )
            is False
        ):
            extra_body = dict(passed_params.pop("extra_body", None) or {})
            for k in passed_params.keys():
                if k not in openai_params and passed_params[k] is not None:
                    extra_body[k] = passed_params[k]
            if not isinstance(optional_params.get("extra_body"), dict):
                optional_params["extra_body"] = {}
            initial_extra_body = {
                **optional_params["extra_body"],
                **extra_body,
            }

            if additional_drop_params is not None:
                processed_extra_body = {
                    k: v
                    for k, v in initial_extra_body.items()
                    if k not in additional_drop_params
                }
            else:
                processed_extra_body = initial_extra_body

            _ensure_extra_body_is_safe = getattr(
                sys.modules[__name__], "_ensure_extra_body_is_safe"
            )
            optional_params["extra_body"] = _ensure_extra_body_is_safe(
                extra_body=processed_extra_body
            )
    else:
        for k in passed_params.keys():
            if k not in openai_params and passed_params[k] is not None:
                if _should_drop_param(
                    k=k, additional_drop_params=additional_drop_params
                ):
                    continue
                optional_params[k] = passed_params[k]
    return optional_params

