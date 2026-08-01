
def should_pad_bench_key(
    match: Match,
    mat1: Tensor,
    mat2: Tensor,
    op: torch._ops.OpOverloadPacket,
    input: Tensor | None = None,
    is_base_time_key: bool = False,
) -> str:
    def tensor_key(t: Tensor) -> tuple[torch.Size, tuple[int, ...], torch.dtype]:
        return (t.shape, t.stride(), t.dtype)

    tf32_key = (
        None
        if mat1.dtype != torch.float32
        else torch.backends.cuda.matmul.fp32_precision == "tf32"
        or torch.backends.mkldnn.fp32_precision == "tf32"
    )

    def fmt_pad(name: str) -> str | None:
        if is_base_time_key:
            return None
        return f"exclude_pad:{should_exclude_padding_time(match, name)}"

    key = (
        tensor_key(mat1),
        tensor_key(mat2),
        fmt_pad("mat1"),
        fmt_pad("mat2"),
        op,
        input if input is None else tensor_key(input),
        tf32_key,
    )

    key = str(key)
    if is_base_time_key:
        key = f"base mm time: {key}"
    return key

