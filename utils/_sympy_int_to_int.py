import math


def _sympy_int_to_int(val: sympy.Expr, adjust: str) -> int | None:
    # Convert simple sympy Integers into concrete int
    if val in (sympy.oo, int_oo):
        return None
    if val in (-sympy.oo, -int_oo):
        return None
    if isinstance(val, sympy.Integer):
        return int(val)

    # TODO: Remove this adjustment when Ed gets rid of fractional ranges
    log.warning(
        "Export constraints cannot be non-integer expressions. Found "
        "type %s, and value %s. We will attempt to %s "
        "this value.",
        type(val),
        val,
        adjust,
    )

    if adjust == "floor":
        return math.floor(val)
    elif adjust == "ceil":
        return math.ceil(val)
    else:
        raise RuntimeError(f"Got invalid adjustment {adjust}")

