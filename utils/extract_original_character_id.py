
def extract_original_character_id(encoded_character_id: str) -> str:
    """Extract original character ID without encoding."""
    decoded = decode_character_id_with_provider(encoded_character_id)
    return decoded.get("character_id", encoded_character_id)

