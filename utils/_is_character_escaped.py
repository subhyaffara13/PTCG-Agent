
def _is_character_escaped(s: str, charpos: int) -> bool:
    num_bslashes = 0
    while (charpos > num_bslashes
           and s[charpos - 1 - num_bslashes] == '\\'):
        num_bslashes += 1
    return num_bslashes % 2 == 1


def _is_character_escaped(s, charpos):
    num_bslashes = 0
    while (charpos > num_bslashes
           and s[charpos - 1 - num_bslashes] == '\\'):
        num_bslashes += 1
    return num_bslashes % 2 == 1

