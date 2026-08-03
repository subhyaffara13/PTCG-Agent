from typing import Optional

def encode_character_id_with_provider(
    character_id: str, provider: str, model_id: Optional[str] = None
) -> str:
    """Encode provider and model_id into character_id using base64."""
    if not provider or not character_id:
        return character_id

    decoded = decode_character_id_with_provider(character_id)
    if decoded.get("custom_llm_provider") is not None:
        return character_id

    assembled_id = CHARACTER_ID_TEMPLATE.format(provider, model_id or "", character_id)
    base64_encoded_id: str = base64.b64encode(assembled_id.encode("utf-8")).decode(
        "utf-8"
    )
    return f"{CHARACTER_ID_PREFIX}{base64_encoded_id}"

