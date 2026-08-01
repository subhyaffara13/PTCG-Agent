
def meta_searchsorted(
    sorted_sequence,
    self,
    *,
    out_int32=False,
    right=False,
    side=None,
    sorter=None,
):
    # If the sorted_sequence is not one-dimensional, its shape must match that of values
    # in all but the last dimension.
    torch._check(
        len(sorted_sequence.shape) <= 1
        or sorted_sequence.shape[:-1] == self.shape[:-1],
        lambda: (
            "torch.searchsorted(): boundaries tensor should be 1 dimension or the "
            "first N-1 dimensions of boundaries tensor and input value tensor must "
            f"match, but we got boundaries tensor {list(sorted_sequence.shape)} and "
            f"input value tensor {list(self.shape)}"
        ),
    )

    # If a sorter array is provided, its dimensions must exactly match sorted_sequence.
    torch._check(
        sorter is None or sorted_sequence.shape == sorter.shape,
        lambda: (
            "torch.searchsorted(): boundary and sorter must have the same size, but "
            f"got boundary tensor {list(sorted_sequence.shape)} and got sorter tensor "
            f"{list(sorter.shape) if sorter is not None else []}"
        ),
    )

    # Per the docs, if side == "left" and right is True, we error.
    torch._check(
        side != "left" or not right,
        lambda: "torch.searchsorted(): side and right can't be set to opposites, got side of "
        "left while right was True",
    )

    dtype = torch.int32 if out_int32 else torch.int64
    if isinstance(self, torch.Tensor):
        return torch.empty_like(
            self, dtype=dtype, memory_format=torch.contiguous_format
        )
    else:  # Scalar
        return torch.empty((), dtype=dtype, device=sorted_sequence.device)

