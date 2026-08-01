
def get_reconstruct_fn(cls: type[OpaqueBase]) -> ReconstructFn | None:
    info = _resolve_opaque_type_info(cls)
    if info is None:
        return None
    return info.reconstruct_fn

