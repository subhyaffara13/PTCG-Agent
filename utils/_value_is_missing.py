from typing import Any

def _value_is_missing(param: click.Parameter, value: Any) -> bool:
    if value is None:
        return True

    # Click 8.3 and beyond
    # if value is UNSET:
    #     return True

    if (param.nargs != 1 or param.multiple) and value == ():
        return True  # pragma: no cover

    return False

