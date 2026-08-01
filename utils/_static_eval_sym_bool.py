
def _static_eval_sym_bool(x: SymBool) -> bool | None:
    if not isinstance(x, SymBool):
        raise AssertionError(f"Expected SymBool, got {type(x)}")
    expr = x.node.expr

    try:
        # Shape env access is inside the try on purpose. xla symnode does not
        # have it on its attributes.
        shape_env = x.node.shape_env
        simplified = shape_env._maybe_evaluate_static(expr)
        if simplified is not None:
            return bool(simplified)
        else:
            return None
    except Exception:
        log.debug("Could not simplify %s", expr)
        return None

