
def functional_mode_key(
    ctx: Any, gm: GraphModule, *args: Any, **kwargs: Any
) -> tuple[torch.Tensor]:
    if kwargs:
        raise AssertionError(f"kwargs must be empty, got {kwargs}")

    unwrapped_inputs = ctx.unwrap_tensors(args)
    with ctx.redispatch_to_next():
        out = local_map_hop(gm, *unwrapped_inputs)
        return ctx.wrap_tensors(out)

