
def bind_symbols(gm: torch.fx.GraphModule, *args: Tensor) -> dict[sympy.Symbol, int]:
    if gm.shape_env is None:
        raise AssertionError("gm.shape_env must not be None")
    return gm.shape_env.bind_symbols(fx_placeholder_vals(gm), args)  # type: ignore[operator, union-attr]

