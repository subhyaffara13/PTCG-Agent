
def decode_video_id_with_provider(encoded_video_id: str) -> DecodedVideoId:
    """Decode provider and model_id from encoded video_id."""
    if not encoded_video_id:
        return DecodedVideoId(
            custom_llm_provider=None,
            model_id=None,
            video_id=encoded_video_id,
        )

    if not encoded_video_id.startswith(VIDEO_ID_PREFIX):
        return DecodedVideoId(
            custom_llm_provider=None,
            model_id=None,
            video_id=encoded_video_id,
        )

    try:
        cleaned_id = encoded_video_id.replace(VIDEO_ID_PREFIX, "")
        cleaned_id = _add_base64_padding(cleaned_id)
        decoded_id = base64.b64decode(cleaned_id.encode("utf-8")).decode("utf-8")

        if ";" not in decoded_id:
            return DecodedVideoId(
                custom_llm_provider=None,
                model_id=None,
                video_id=encoded_video_id,
            )

        parts = decoded_id.split(";")

        custom_llm_provider = None
        model_id = None
        decoded_video_id = encoded_video_id

        if len(parts) >= 3:
            custom_llm_provider_part = parts[0]
            model_id_part = parts[1]
            video_id_part = parts[2]

            custom_llm_provider = custom_llm_provider_part.replace(
                "litellm:custom_llm_provider:", ""
            )
            model_id = model_id_part.replace("model_id:", "")
            decoded_video_id = video_id_part.replace("video_id:", "")

        return DecodedVideoId(
            custom_llm_provider=custom_llm_provider,
            model_id=model_id,
            video_id=decoded_video_id,
        )
    except Exception as e:
        verbose_logger.debug(f"Error decoding video_id '{encoded_video_id}': {e}")
        return DecodedVideoId(
            custom_llm_provider=None,
            model_id=None,
            video_id=encoded_video_id,
        )

