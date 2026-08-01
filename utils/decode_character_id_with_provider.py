
def decode_character_id_with_provider(encoded_character_id: str) -> DecodedCharacterId:
    """Decode provider and model_id from encoded character_id."""
    if not encoded_character_id:
        return DecodedCharacterId(
            custom_llm_provider=None,
            model_id=None,
            character_id=encoded_character_id,
        )

    if not encoded_character_id.startswith(CHARACTER_ID_PREFIX):
        return DecodedCharacterId(
            custom_llm_provider=None,
            model_id=None,
            character_id=encoded_character_id,
        )

    try:
        cleaned_id = encoded_character_id.replace(CHARACTER_ID_PREFIX, "")
        cleaned_id = _add_base64_padding(cleaned_id)
        decoded_id = base64.b64decode(cleaned_id.encode("utf-8")).decode("utf-8")

        if ";" not in decoded_id:
            return DecodedCharacterId(
                custom_llm_provider=None,
                model_id=None,
                character_id=encoded_character_id,
            )

        parts = decoded_id.split(";")

        custom_llm_provider = None
        model_id = None
        decoded_character_id = encoded_character_id

        if len(parts) >= 3:
            custom_llm_provider_part = parts[0]
            model_id_part = parts[1]
            character_id_part = parts[2]

            custom_llm_provider = custom_llm_provider_part.replace(
                "litellm:custom_llm_provider:", ""
            )
            model_id = model_id_part.replace("model_id:", "")
            decoded_character_id = character_id_part.replace("character_id:", "")

        return DecodedCharacterId(
            custom_llm_provider=custom_llm_provider,
            model_id=model_id,
            character_id=decoded_character_id,
        )
    except Exception as e:
        verbose_logger.debug(
            f"Error decoding character_id '{encoded_character_id}': {e}"
        )
        return DecodedCharacterId(
            custom_llm_provider=None,
            model_id=None,
            character_id=encoded_character_id,
        )

