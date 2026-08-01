
def is_hangul(character: str) -> bool:
    return bool(_character_flags(character) & _HANGUL)

