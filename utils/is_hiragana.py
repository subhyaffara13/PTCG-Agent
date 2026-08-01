
def is_hiragana(character: str) -> bool:
    return bool(_character_flags(character) & _HIRAGANA)

