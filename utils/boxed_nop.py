
def boxed_nop(
    fx_g: torch.fx.GraphModule, example_inputs: list[torch.Tensor]
) -> Callable[..., Any]:
    from torch.fx.graph import _BoxedCodeGen

    # Set the graph to use boxed codegen
    fx_g.graph.set_codegen(_BoxedCodeGen())
    fx_g.recompile()

    if functorch_config.force_autograd_cache or functorch_config.bundled_autograd_cache:
        result = AOTEagerOutputCode(gm=fx_g)
        result._boxed_call = True  # type: ignore[attr-defined]
        return result

    # Wrap the forward method in a function so we can set _boxed_call attribute
    forward_fn = fx_g.forward

    def run(args: Any) -> Any:
        from torch.utils._debug_mode import DebugInterpreter, get_active_debug_mode

        if (
            debug_mode := get_active_debug_mode()
        ) is not None and debug_mode.run_compile_with_interpreter:
            return DebugInterpreter(fx_g, backend="aot_eager").run(*args)
        return forward_fn(args)

    run._boxed_call = True  # type: ignore[attr-defined]
    return run

