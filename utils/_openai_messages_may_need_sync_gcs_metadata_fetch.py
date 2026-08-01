
def _openai_messages_may_need_sync_gcs_metadata_fetch(
    messages: List[AllMessageValues],
) -> bool:
    """
    Heuristic: True if any message part can trigger a blocking GCS JSON
    metadata read inside _transform_request_body (extension-less gs:// without
    explicit MIME hints). Covers user/system ``content`` parts and assistant
    ``images`` (same paths as ``_gemini_convert_messages_with_history``). Used
    to decide whether ``async_transform_request_body`` should offload the sync
    transform via ``asyncify``.
    """
    for raw in messages:
        msg: Any = raw
        if not isinstance(msg, dict) and hasattr(msg, "model_dump"):
            msg = msg.model_dump(exclude_none=False)
        if not isinstance(msg, dict):
            continue
        images_field = msg.get("images")
        if isinstance(images_field, list):
            for image_item in images_field:
                if not isinstance(image_item, dict):
                    continue
                if _image_url_payload_may_need_sync_gcs_metadata_fetch(
                    image_item.get("image_url")
                ):
                    return True

        content = msg.get("content")
        if not isinstance(content, list):
            continue
        for item in content:
            if not isinstance(item, dict):
                continue
            itype = item.get("type")
            if itype == "image_url":
                if _image_url_payload_may_need_sync_gcs_metadata_fetch(
                    item.get("image_url")
                ):
                    return True
            elif itype == "file":
                file_obj = item.get("file")
                if not isinstance(file_obj, dict):
                    continue
                fmt = (
                    file_obj.get("format")
                    or file_obj.get("mime_type")
                    or file_obj.get("content_type")
                )
                passed = file_obj.get("file_id") or file_obj.get("file_data")
                if (
                    isinstance(passed, str)
                    and "gs://" in passed
                    and not fmt
                    and _gs_uri_requires_content_type_metadata(passed)
                ):
                    return True
    return False

