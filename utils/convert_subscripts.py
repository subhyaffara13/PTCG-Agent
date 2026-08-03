from typing import Any, Dict, List

def convert_subscripts(old_sub: List[Any], symbol_map: Dict[Any, Any]) -> str:
    """Convert user custom subscripts list to subscript string according to `symbol_map`.

    Examples:
    --------
    >>>  oe.parser.convert_subscripts(['abc', 'def'], {'abc':'a', 'def':'b'})
    'ab'
    >>> oe.parser.convert_subscripts([Ellipsis, object], {object:'a'})
    '...a'
    """
    new_sub = ""
    for s in old_sub:
        if s is Ellipsis:
            new_sub += "..."
        else:
            # no need to try/except here because symbol_map has already been checked
            new_sub += symbol_map[s]
    return new_sub

