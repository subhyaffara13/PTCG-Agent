
def fetch_sym_proxy(
    tracer: _ProxyTracer,
) -> Callable[[PySymType], bool | int | float | Proxy]:
    def inner(e: PySymType) -> int | bool | float | Proxy:
        n = e.node
        if n.constant is not None:
            return n.constant
        if e.node.expr.is_number:
            if isinstance(e, SymBool):
                return bool(e.node.expr)
            elif isinstance(e, SymInt):
                return int(e.node.expr)
            return float(e.node.expr)
        else:
            if not isinstance(e, py_sym_types):
                raise AssertionError(f"Expected py_sym_types, got {type(e)}")
            # NB: we REQUIRE all symints to be tracked
            return get_proxy_slot(e, tracer).force()

    return inner

