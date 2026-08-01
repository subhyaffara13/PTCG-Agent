
def count_flops_fx(node: torch.fx.Node) -> int | None:
    if not countable_fx(node) or isinstance(node.target, str):
        return None
    with FakeTensorMode(allow_non_fake_inputs=True):
        success, args, kwargs = get_fake_args_kwargs(node)

        if success:
            with torch.utils.flop_counter.FlopCounterMode(
                display=False
            ) as flop_counter_mode:
                node.target(*args, **kwargs)

            counted_flops = flop_counter_mode.get_total_flops()
            return counted_flops
    return None

