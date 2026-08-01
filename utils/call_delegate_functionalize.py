
def call_delegate_functionalize(
    ctx,
    lowered_module: AOTI_LOWERED_MODULE,  # type: ignore[valid-type]
    original_gm: torch.fx.GraphModule,
    weight_args: list[torch.Tensor],
    input_args: list[torch.Tensor],
):
    unwrapped_weight_args = tuple(
        ctx.unwrap_tensors(weight_arg) for weight_arg in weight_args
    )
    unwrapped_input_args = tuple(
        ctx.unwrap_tensors(input_arg) for input_arg in input_args
    )
    with ctx.redispatch_to_next():
        res = aoti_call_delegate(
            lowered_module,
            original_gm,
            unwrapped_weight_args,  # type: ignore[arg-type]
            unwrapped_input_args,  # type: ignore[arg-type]
        )
        return ctx.wrap_tensors(res)


def call_delegate_functionalize(ctx, lowered_module, *args):
    unwrapped_args = tuple(ctx.unwrap_tensors(arg) for arg in args)
    with ctx.redispatch_to_next():
        res = executorch_call_delegate(lowered_module, *unwrapped_args)
        return ctx.wrap_tensors(res)

