
def encode_video_id_with_provider(
    video_id: str, provider: str, model_id: Optional[str] = None
) -> str:
    """Encode provider and model_id into video_id using base64."""
    if not provider or not video_id:
        return video_id

    # Try to decode the ID first to check if it's already encoded
    # This handles the case where Azure/OpenAI return IDs that start with "video_"
    # but are not yet encoded with provider information
    decoded = decode_video_id_with_provider(video_id)
    if decoded.get("custom_llm_provider") is not None:
        # ID is already encoded, return as-is
        return video_id

    # ID is not encoded (even if it starts with video_), so encode it
    assembled_id = str(SpecialEnums.LITELLM_MANAGED_VIDEO_COMPLETE_STR.value).format(
        provider, model_id or "", video_id
    )

    base64_encoded_id: str = base64.b64encode(assembled_id.encode("utf-8")).decode(
        "utf-8"
    )

    return f"{VIDEO_ID_PREFIX}{base64_encoded_id}"

