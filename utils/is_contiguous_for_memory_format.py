
def is_contiguous_for_memory_format(  # type: ignore[return]
    a: Tensor,
    *,
    memory_format: torch.memory_format,
    false_if_dde=False,
    # pyrefly: ignore [bad-return]
) -> bool:
    validate_memory_format(memory_format)

    if memory_format == torch.contiguous_format:
        return is_contiguous(a, false_if_dde)
    if memory_format == torch.channels_last:
        return is_channels_last_contiguous_2d(a, false_if_dde)
    if memory_format == torch.channels_last_3d:
        return is_channels_last_contiguous_3d(a, false_if_dde)

    torch._check(
        False,
        lambda: f"is_contiguous received unsupported memory format {memory_format}",
    )

