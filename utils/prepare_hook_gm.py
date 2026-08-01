
def prepare_hook_gm(
    aot_config: AOTConfig, fn: Callable[..., Any], args: tuple[Any, ...]
) -> torch.fx.GraphModule:
    from torch._functorch._aot_autograd.graph_capture import _create_graph

    fn, args = create_wrap_fn(fn, args)
    gm = _create_graph(fn, args, aot_config=aot_config)  # type: ignore[arg-type]
    return gm

