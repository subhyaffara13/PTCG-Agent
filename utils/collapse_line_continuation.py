import re

def collapse_line_continuation(l: list[str]) -> list[str]:
    r: list[str] = []
    cont = False
    for s in l:
        ss = re.sub(r"\\$", "", s)
        if cont:
            r[-1] += re.sub("^ +", "", ss)
        else:
            r.append(ss)
        cont = s.endswith("\\")
    return r

