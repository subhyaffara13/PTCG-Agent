
def _ensure_litellm_metadata(data: dict, user_api_key_dict: UserAPIKeyAuth) -> None:
    """Populate data['litellm_metadata'] from user_api_key_dict if absent."""
    if "litellm_metadata" not in data:
        from litellm.llms.base_llm.guardrail_translation.base_translation import (
            BaseTranslation,
        )

        user_metadata = BaseTranslation.transform_user_api_key_dict_to_metadata(
            user_api_key_dict
        )
        if user_metadata:
            data["litellm_metadata"] = user_metadata

