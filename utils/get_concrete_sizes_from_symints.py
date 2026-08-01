
def get_concrete_sizes_from_symints(msg: str, fake_mode: FakeTensorMode | None) -> str:
    """
    Replace symbolic size expressions (like 's0', 's94') in error messages
    with their concrete runtime values for better readability.

    Example: "size (s94)" -> "size (s94: hint= 10)" if s94's value is 10.
    """
    import re

    from sympy.core.numbers import Integer

    if fake_mode is None:
        return msg

    pattern = r"\(s(\d+)\)"
    assert fake_mode.shape_env is not None
    shape_env = fake_mode.shape_env
    backed_var_to_val = shape_env.backed_var_to_val

    def replace_sym(match: Any) -> str:
        sym_name = f"s{match.group(1)}"
        val = next(
            (v for k, v in backed_var_to_val.items() if k.name == sym_name),
            None,
        )
        if isinstance(val, (int, Integer)):
            return f"({sym_name}: hint = {str(val)})"
        return match.group(0)

    msg = re.sub(pattern, replace_sym, msg)
    return msg

