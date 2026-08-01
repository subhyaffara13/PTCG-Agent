
def fetch_object_proxy(tracer: _ProxyTracer, t: Tensor) -> _ProxyTensor | Tensor: ...


def fetch_object_proxy(
    tracer: _ProxyTracer, t: _AnyScriptObjectType
) -> Proxy | _AnyScriptObjectType: ...


def fetch_object_proxy(
    tracer: _ProxyTracer, t: PySymType
) -> _PySymProxyType | PySymType: ...


def fetch_object_proxy(
    tracer: _ProxyTracer, t: OpaqueBase
) -> _OpaqueObjectProxyType | PySymType: ...


def fetch_object_proxy(
    tracer: _ProxyTracer,
    t: Tensor | _AnyScriptObjectType | PySymType | OpaqueBase,
) -> object:
    return get_proxy_slot(t, tracer, t)

