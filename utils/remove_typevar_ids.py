import re

def remove_typevar_ids(a: list[str]) -> list[str]:
    return [re.sub(r"`-?\d+", "", line) for line in a]

