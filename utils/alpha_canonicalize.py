from typing import Dict

def alpha_canonicalize(equation: str) -> str:
    """Alpha convert an equation in an order-independent canonical way.

    Examples:
    --------
    >>> oe.parser.alpha_canonicalize("dcba")
    'abcd'

    >>> oe.parser.alpha_canonicalize("Ĥěļļö")
    'abccd'
    """
    rename: Dict[str, str] = {}
    for name in equation:
        if name in ".,->":
            continue
        if name not in rename:
            rename[name] = get_symbol(len(rename))
    return "".join(rename.get(x, x) for x in equation)

