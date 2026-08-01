
def is_cjk(character: str) -> bool:
    return bool(_character_flags(character) & _CJK)

