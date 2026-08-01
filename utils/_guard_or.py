
def _guard_or(a: BoolLikeType, default: bool) -> bool:
    """
    Try to guard a, if data dependent error encountered just return default.
    """
    if not isinstance(a, SymBool):
        if not isinstance(a, bool):
            raise AssertionError(f"Expected bool, got {type(a)}")
        return a

    # if backed_size_oblivious is True we treat backed as unbacked here.
    if torch.fx.experimental._config.backed_size_oblivious:
        result = _static_eval_sym_bool(a)
        return result if result is not None else default

    shape_env = getattr(a.node, "shape_env", None)

    # xla symnode path.
    if shape_env is None:
        return guard_bool(a)

    sym_node = a.node
    r = sym_node.shape_env.evaluate_sym_node(
        sym_node, size_oblivious=False, fallback_value=default
    )
    return bool(r)

