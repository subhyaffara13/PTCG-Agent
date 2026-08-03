import re

def parse_all_signatures(lines: Sequence[str]) -> tuple[list[Sig], list[Sig]]:
    """Parse all signatures in a given reST document.

    Return lists of found signatures for functions and classes.
    """
    sigs = []
    class_sigs = []
    for line in lines:
        line = line.strip()
        m = re.match(r"\.\. *(function|method|class) *:: *[a-zA-Z_]", line)
        if m:
            sig = line.split("::")[1].strip()
            parsed = parse_signature(sig)
            if parsed:
                name, fixed, optional = parsed
                if m.group(1) != "class":
                    sigs.append((name, build_signature(fixed, optional)))
                else:
                    class_sigs.append((name, build_signature(fixed, optional)))

    return sorted(sigs), sorted(class_sigs)

