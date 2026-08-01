
def statically_known_true(
    shape_env: ShapeEnv,
    expr: sympy.Basic | bool,
    axioms: tuple[sympy.Expr] | None = None,
    var_to_range: tuple[tuple[sympy.Symbol, ValueRanges[Any]]] | None = None,
) -> bool:
    if expr in (True, False):
        return bool(expr)

    try:
        simplified = shape_env._maybe_evaluate_static(
            expr,
            axioms=axioms,
            var_to_range=var_to_range,
        )
        if simplified is not None:
            return bool(simplified)
    except Exception:
        log.debug("Could not simplify  %s", expr, exc_info=True)

    return False


def statically_known_true(x: BoolLikeType) -> bool:
    """
    Returns True if x can be simplified to a constant and is true.

    .. note::
        This function doesn't introduce new guards, so the expression may end
        up evaluating to true at runtime even if this function returns False.

    Args:
        x (bool, SymBool): The expression to try statically evaluating
    """
    if not isinstance(x, SymBool):
        if not isinstance(x, bool):
            raise AssertionError(f"Expected bool, got {type(x)}")
        return x
    result = _static_eval_sym_bool(x)
    if result is None:
        return False

    return result

