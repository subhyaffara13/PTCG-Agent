from typing import Any, List, Optional

def _extract_models_from_managed_resource_id(
    resource_id: Any,
    resource_id_field: Optional[str] = None,
    llm_router: Optional[Router] = None,
) -> List[str]:
    if not isinstance(resource_id, str) or not resource_id:
        return []

    candidates: List[str] = []

    try:
        from litellm.proxy.openai_files_endpoints.common_utils import (
            _is_base64_encoded_unified_file_id,
            decode_model_from_file_id,
            get_model_id_from_unified_batch_id,
            get_models_from_unified_file_id,
        )

        _append_model_candidates(
            candidates=candidates, value=decode_model_from_file_id(resource_id)
        )
        unified_file_id = _is_base64_encoded_unified_file_id(resource_id)
        if unified_file_id:
            _append_model_candidates(
                candidates=candidates,
                value=get_models_from_unified_file_id(unified_file_id),
            )
            _append_model_candidates(
                candidates=candidates,
                value=get_model_id_from_unified_batch_id(unified_file_id),
            )
    except Exception as e:
        verbose_proxy_logger.debug(
            "Unable to extract model from managed file/batch ID: %s", str(e)
        )

    try:
        from litellm.llms.base_llm.managed_resources.utils import parse_unified_id

        parsed_id = parse_unified_id(resource_id)
        if parsed_id:
            _append_model_candidates(
                candidates=candidates, value=parsed_id.get("model_id")
            )
            _append_model_candidates(
                candidates=candidates, value=parsed_id.get("target_model_names")
            )
    except Exception as e:
        verbose_proxy_logger.debug(
            "Unable to extract model from unified managed resource ID: %s", str(e)
        )

    if resource_id_field in ("video_id", "character_id"):
        try:
            from litellm.types.videos.utils import (
                decode_character_id_with_provider,
                decode_video_id_with_provider,
            )

            if resource_id_field == "video_id":
                model_id = decode_video_id_with_provider(resource_id).get("model_id")
                _append_model_candidates(
                    candidates=candidates,
                    value=_resolve_model_id_with_router(model_id, llm_router),
                )
            else:
                model_id = decode_character_id_with_provider(resource_id).get(
                    "model_id"
                )
                _append_model_candidates(
                    candidates=candidates,
                    value=_resolve_model_id_with_router(model_id, llm_router),
                )
        except Exception as e:
            verbose_proxy_logger.debug(
                "Unable to extract model from managed video/character ID: %s", str(e)
            )

    return _dedupe_model_candidates(candidates)

