
def upload_bytes_sync(
    raw_bytes: bytes,
    mime: Optional[str],
    api_key: str,
    api_base: Optional[str],
) -> str:
    import litellm

    response = litellm.module_level_client.post(
        url="{}{}".format(_normalize_api_base(api_base), "/upload"),
        headers={"Authorization": f"Bearer {api_key}"},
        files={"file": ("document", raw_bytes, mime or "application/octet-stream")},
        timeout=request_timeout,
    )
    response.raise_for_status()
    return _extract_file_id_from_upload_response(response)

