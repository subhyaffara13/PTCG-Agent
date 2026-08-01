
def materialize_as_graph(
    fn: Callable,
    args: tuple[Any, ...],
    include_key_set: torch._C.DispatchKeySet | None = None,
    exclude_key_set: torch._C.DispatchKeySet | None = None,
    force_enable_grad=False,
    subgraph_decomp_table: Mapping[OpOverload, Callable] | None = None,
) -> torch.fx.GraphModule:
    if include_key_set is None:
        include_key_set = torch._C._dispatch_tls_local_include_set()
    if exclude_key_set is None:
        exclude_key_set = torch._C._dispatch_tls_local_exclude_set()

    @torch._dynamo.disable(recursive=True, reason=None)
    def _materialize_as_graph_inner():
        from torch._guards import active_fake_mode
        from torch.fx.experimental.proxy_tensor import _CURRENT_MAKE_FX_TRACER

        with suspend_functionalization(), disable_functional_mode():
            fake_mode = None
            if _CURRENT_MAKE_FX_TRACER is not None:
                fake_mode = _CURRENT_MAKE_FX_TRACER.fake_tensor_mode
            if fake_mode is None:
                fake_mode = active_fake_mode()

            with contextlib.ExitStack() as stack:
                stack.enter_context(
                    torch.utils._python_dispatch._disable_current_modes()
                )
                if fake_mode is not None:
                    stack.enter_context(fake_mode)

                with disable_proxy_modes_tracing():
                    unfunc_t = [_from_fun(arg) for arg in args]

                stack.enter_context(
                    torch._C._ForceDispatchKeyGuard(include_key_set, exclude_key_set),
                )
                if force_enable_grad:
                    stack.enter_context(torch.enable_grad())
                return _maybe_reenter_make_fx(
                    fn, subgraph_decomp_table=subgraph_decomp_table
                )(*unfunc_t)

    gm = _materialize_as_graph_inner()
    if gm is None:
        raise AssertionError("materialize_as_graph returned None")
    return gm

