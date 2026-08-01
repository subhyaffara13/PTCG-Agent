
def has_proxy_slot(obj: Tensor, tracer: _ProxyTracer) -> bool:
    if not isinstance(obj, (Tensor, SymNode)):
        raise AssertionError(f"Expected Tensor or SymNode, got {type(obj)}")

    return bool(get_proxy_slot(obj, tracer, False, lambda _: True))

