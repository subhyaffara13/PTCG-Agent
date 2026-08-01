
def eval_guards(
    gm: torch.fx.GraphModule, *args: Tensor, ignore_static: bool = True
) -> bool:
    if gm.shape_env is None:
        raise AssertionError("gm.shape_env must not be None")
    return gm.shape_env.evaluate_guards_for_args(  # type: ignore[operator, union-attr]
        fx_placeholder_vals(gm), args, ignore_static=ignore_static
    )

