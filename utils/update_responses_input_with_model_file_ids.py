from typing import Any, Dict, List, Optional, Union

def update_responses_input_with_model_file_ids(
    input: Any,
    model_id: Optional[str] = None,
    model_file_id_mapping: Optional[Dict[str, Dict[str, str]]] = None,
) -> Union[str, List[Dict[str, Any]]]:
    """
    Updates responses API input with provider-specific file IDs.
    File IDs are always inside the content array, not as direct input_file items.

    For managed files (unified file IDs), uses model_file_id_mapping if provided,
    otherwise decodes the base64-encoded unified file ID and extracts the llm_output_file_id directly.

    Args:
        input: The responses API input parameter
        model_id: The model ID to use for looking up provider-specific file IDs
        model_file_id_mapping: Dictionary mapping litellm file IDs to provider file IDs
                               Format: {"litellm_file_id": {"model_id": "provider_file_id"}}
    """
    from litellm.proxy.openai_files_endpoints.common_utils import (
        _is_base64_encoded_unified_file_id,
        convert_b64_uid_to_unified_uid,
    )

    if isinstance(input, str):
        return input

    if not isinstance(input, list):
        return input

    updated_input = []
    for item in input:
        if not isinstance(item, dict):
            updated_input.append(item)
            continue

        updated_item = item.copy()
        content = item.get("content")
        if isinstance(content, list):
            updated_content = []
            for content_item in content:
                if (
                    isinstance(content_item, dict)
                    and content_item.get("type") == "input_file"
                ):
                    file_id = content_item.get("file_id")
                    if file_id:
                        provider_file_id = file_id  # Default to original

                        # Check if we have a mapping for this file ID
                        if (
                            model_file_id_mapping
                            and model_id
                            and file_id in model_file_id_mapping
                        ):
                            # Use the model-specific file ID from mapping
                            provider_file_id = (
                                model_file_id_mapping.get(file_id, {}).get(model_id)
                                or file_id
                            )
                            updated_content_item = content_item.copy()
                            updated_content_item["file_id"] = provider_file_id
                            updated_content.append(updated_content_item)
                        else:
                            # Check if this is a base64-encoded unified file ID without mapping
                            is_unified_file_id = _is_base64_encoded_unified_file_id(
                                file_id
                            )
                            if is_unified_file_id:
                                # Fallback: decode unified file ID
                                unified_file_id = convert_b64_uid_to_unified_uid(
                                    file_id
                                )
                                if "llm_output_file_id," in unified_file_id:
                                    provider_file_id = unified_file_id.split(
                                        "llm_output_file_id,"
                                    )[1].split(";")[0]

                                updated_content_item = content_item.copy()
                                updated_content_item["file_id"] = provider_file_id
                                updated_content.append(updated_content_item)
                            else:
                                # Not a managed file, keep as-is
                                updated_content.append(content_item)
                    else:
                        updated_content.append(content_item)
                else:
                    updated_content.append(content_item)
            updated_item["content"] = updated_content

        updated_input.append(updated_item)

    return updated_input

