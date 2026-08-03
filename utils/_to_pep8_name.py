import re

def _to_pep8_name(s: str, _re_sub_pattern=re.compile(r"([a-z])([A-Z])")) -> str:
    s = _re_sub_pattern.sub(r"\1_\2", s)
    return s.lower()

