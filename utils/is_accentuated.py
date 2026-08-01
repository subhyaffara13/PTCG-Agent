
def is_accentuated(character: str) -> bool:
    return bool(_character_flags(character) & _ACCENTUATED)

