
def set_meta(proxy: Proxy, val: _ExtractValType) -> Proxy:
    proxy.node.meta["val"] = extract_val(
        val, include_real=(proxy.node.op == "placeholder")
    )

    with _enable_thunkify(proxy.tracer):  # type: ignore[arg-type]
        # Best effort tensor_meta setting; prefer using val!
        if is_fake(val):
            proxy.node.meta["tensor_meta"] = _extract_tensor_metadata(val)
        elif isinstance(val, Tensor) and not val.is_sparse:
            proxy.node.meta["tensor_meta"] = _extract_tensor_metadata(val)
    return proxy

