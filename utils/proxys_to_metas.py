
def proxys_to_metas(v):
    if isinstance(v, MetaDeviceAttribute):
        return "meta"
    if isinstance(v, torch.fx.Proxy):
        if not isinstance(v, MetaProxy):
            raise AssertionError(f"Expected MetaProxy but got {type(v)}")
        if not hasattr(v, "_tensor_meta"):
            raise AssertionError("MetaProxy does not have an associated meta")
        return v._tensor_meta
    return v

