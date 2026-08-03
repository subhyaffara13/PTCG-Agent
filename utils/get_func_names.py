import re

def get_func_names(expected: list[str]) -> list[str]:
    res = []
    for s in expected:
        m = re.match(r"def ([_a-zA-Z0-9.*$]+)\(", s)
        if m:
            res.append(m.group(1))
    return res

