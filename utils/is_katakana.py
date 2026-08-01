
def is_katakana(character: str) -> bool:
    return bool(_character_flags(character) & _KATAKANA)

