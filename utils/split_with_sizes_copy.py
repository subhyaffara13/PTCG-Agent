
def split_with_sizes_copy(
    self: Tensor,
    split_sizes: list[int],
    dim: int = 0,
    out: list[Tensor] | None = None,
) -> list[Tensor] | None:
    splits = aten.split_with_sizes(self, split_sizes, dim=dim)
    if out is None:
        return [s.clone(memory_format=torch.contiguous_format) for s in splits]
    else:
        for output, split in zip(out, splits):
            _maybe_resize_out(output, split.shape)
            _safe_copy_out(copy_from=split, copy_to=output, exact_dtype=True)
        return None


def split_with_sizes_copy(
    all_gather_output: torch.Tensor,
    all_gather_input_split_sizes: list[int],
    dim: int = 0,
    *,
    out: list[torch.Tensor],
) -> None:
    torch.split_with_sizes_copy(
        all_gather_output, all_gather_input_split_sizes, dim=dim, out=out
    )

