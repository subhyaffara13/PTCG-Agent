
def _extract_tensor_metadata_for_node_hash(
    x: torch.Tensor,
) -> tuple[Callable[[T], T], tuple[Any, ...]]:
    from torch._inductor.codecache import _ident, extract_tensor_metadata_for_cache_key

    out = []
    metadata = extract_tensor_metadata_for_cache_key(x)
    for field in fields(metadata):
        out.append(getattr(metadata, field.name))

    return (_ident, tuple(out))

