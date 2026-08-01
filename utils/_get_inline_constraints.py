
def _get_inline_constraints(fake_mode: FakeTensorMode):
    if fake_mode.shape_env is None:
        raise AssertionError("fake_mode.shape_env must not be None")
    return {
        k: v
        for k, v in fake_mode.shape_env.var_to_range.items()
        if free_unbacked_symbols(k)
    }

