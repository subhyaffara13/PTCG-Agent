
def _validate_symbolic_output_for_caching(
    state: _CacheKeyState, output: FakeTensor
) -> None:
    """
    Validate symbolic content in output and raise _BypassDispatchCache if
    caching should be bypassed.

    Args:
        state: Cache key state containing known symbols
        output: Output to validate
        proxy_mode_active: Whether PROXY dispatch mode is currently active

    Raises: _BypassDispatchCache: If output contains symbolic content that
        prevents caching

    Details:

    If our output contains any symbols that didn't appear in the input then we
    need to bypass. Usually this will be unbacked symbols which can't be
    properly reconstructed but there could be "weird" cases where backed symbols
    spontaneously appear (from non-input state)?

    If we're proxy (symbol) tracing and the output contains ANY symbols then we
    need to bypass. The problem is that ProxyTorchDispatchMode relies on SymNode
    object identity and being able to see the construction of SymNodes.

    We could improve the proxy tracing case in a few ways:

    1. If the output SymNodes are directly copied from inputs then this is
       actually fine - they're already tracked. This would probably be the
       biggest bang/buck.

    2. If the output (tensors) are all direct copies of the inputs then this is
       also fine - since they're inputs they must be tracked. We already compute
       this we just don't plumb it around enough.

    3. If the output SymNodes are already tracked by the proxy then this is also
       actually fine - they're properly tracked. This probably wouldn't be
       common since for most outputs we use torch.empty_strided() and recompute
       strides.

    4. We could use the proxy to track "how" the SymNodes were computed and when
       using the cache we could "replay" them properly to teach the proxy how to
       build them.
    """
    from torch.fx.experimental.symbolic_shapes import _iterate_exprs, _iterate_nodes

    is_tracing = torch.fx.experimental.proxy_tensor.get_proxy_mode() is not None
    if is_tracing:
        # Check for SymNode types in PROXY mode - this should bypass caching
        # regardless of whether symbols are known or not
        for _ in _iterate_nodes(output):
            raise _BypassDispatchCache("Proxy mode with SymNode output")
    else:
        # Check for unrepresented symbols in tensor expressions
        for s in _iterate_exprs(output):
            for symbol in s.free_symbols:
                if symbol not in state.known_symbols:
                    raise _BypassDispatchCache("unrepresented symbol in output")

