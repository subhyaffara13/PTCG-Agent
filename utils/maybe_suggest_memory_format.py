
def maybe_suggest_memory_format(
    t: Tensor, with_memory_format: bool
) -> MemoryFormatMeta | None:
    if not with_memory_format:
        return None

    return MemoryFormatMeta.from_tensor(t)

