
def is_arabic(character: str) -> bool:
    return bool(_character_flags(character) & _ARABIC)

