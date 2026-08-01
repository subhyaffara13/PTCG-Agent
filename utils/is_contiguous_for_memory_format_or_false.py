
def is_contiguous_for_memory_format_or_false(  # type: ignore[return]
    a: Tensor, *, memory_format: torch.memory_format
) -> bool:
    return is_contiguous_for_memory_format(
        a, memory_format=memory_format, false_if_dde=True
    )

