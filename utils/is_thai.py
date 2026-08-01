
def is_thai(character: str) -> bool:
    return bool(_character_flags(character) & _THAI)

