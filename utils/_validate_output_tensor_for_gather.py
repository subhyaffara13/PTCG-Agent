
def _validate_output_tensor_for_gather(
    my_rank: int,
    dst_rank: int,
    size: torch.Size,
    dst_tensor: torch.Tensor | None,
) -> None:
    if dst_rank == my_rank:
        if dst_tensor is None:
            raise ValueError(
                f"Argument ``dst_tensor`` must be specified on destination rank {dst_rank}"
            )
        if tuple(size) != (dst_tensor.size()):
            raise ValueError(
                f"Argument ``dst_tensor`` have size {tuple(dst_tensor.size())},"
                f"but should be {tuple(size)}"
            )
    elif dst_tensor:
        raise ValueError(
            "Argument ``dst_tensor`` must NOT be specified on non-destination ranks."
        )

