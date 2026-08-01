
def is_latin(character: str) -> bool:
    return bool(_character_flags(character) & _LATIN)

