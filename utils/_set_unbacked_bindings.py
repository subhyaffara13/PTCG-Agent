
def _set_unbacked_bindings(out: object, out_proxy: _NestedProxys) -> None:
    """A helper function for setting up unbacked_bindings on the destination FX graph."""
    from .symbolic_shapes import compute_unbacked_bindings

    # Can't use detect_fake_mode here,
    #
    # python test/distributed/_tensor/test_dtensor_compile.py -k
    # test_tp_compile_fullgraph_is_seq_parallel_False
    #
    # will fail.  Very strange, it probably isn't right for them to be using
    # two fake modes there...
    fake_mode = torch._C._get_dispatch_mode(torch._C._TorchDispatchModeKey.FAKE)
    if fake_mode and fake_mode.shape_env:
        if symbol_to_path := compute_unbacked_bindings(fake_mode.shape_env, out):
            if not isinstance(out_proxy, Proxy):
                raise AssertionError(f"Expected Proxy, got {out_proxy}")
            out_proxy.node.meta["unbacked_bindings"] = symbol_to_path

