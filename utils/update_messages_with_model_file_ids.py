
def update_messages_with_model_file_ids(
    messages: List[AllMessageValues],
    model_id: str,
    model_file_id_mapping: Dict[str, Dict[str, str]],
) -> List[AllMessageValues]:
    """
    Updates messages with model file ids.

    For managed files (unified file IDs), uses model_file_id_mapping if it
    resolves the id, otherwise decodes the base64-encoded unified file ID
    and extracts the llm_output_file_id directly. Mirrors the Responses-API
    sibling `update_responses_input_with_model_file_ids`.

    model_file_id_mapping: Dict[str, Dict[str, str]] = {
        "litellm_proxy/file_id": {
            "model_id": "provider_file_id"
        }
    }
    """
    from litellm.proxy.openai_files_endpoints.common_utils import (
        _is_base64_encoded_unified_file_id,
        convert_b64_uid_to_unified_uid,
    )

    for message in messages:
        if message.get("role") == "user":
            content = message.get("content")
            if content:
                if isinstance(content, str):
                    continue
                for c in content:
                    if not isinstance(c, dict):
                        # Content list items aren't always dicts. e.g.
                        # text_completion forwards a token-ids list/list-of-
                        # lists through this path. Skip non-dict items
                        # instead of indexing into them.
                        continue
                    if c.get("type") == "file":
                        file_object = cast(ChatCompletionFileObject, c)
                        file_object_file_field = file_object.get("file")
                        if not isinstance(file_object_file_field, dict):
                            # Content block has `type: "file"` but not the
                            # OpenAI Chat Completions shape (e.g. a LangChain
                            # v1 standardized file block, or a provider-native
                            # shape that also uses `type: "file"`). Nothing to
                            # remap here, so skip instead of crashing.
                            continue
                        file_id = file_object_file_field.get("file_id")
                        format = file_object_file_field.get(
                            "format", get_format_from_file_id(file_id)
                        )

                        if file_id:
                            provider_file_id = (
                                model_file_id_mapping.get(file_id, {}).get(model_id)
                                if model_file_id_mapping
                                else None
                            )
                            if (
                                not provider_file_id
                                and _is_base64_encoded_unified_file_id(file_id)
                            ):
                                unified_file_id = convert_b64_uid_to_unified_uid(
                                    file_id
                                )
                                if "llm_output_file_id," in unified_file_id:
                                    provider_file_id = unified_file_id.split(
                                        "llm_output_file_id,"
                                    )[1].split(";")[0]
                            file_object_file_field["file_id"] = (
                                provider_file_id or file_id
                            )
                        if format:
                            file_object_file_field["format"] = format
    return messages

