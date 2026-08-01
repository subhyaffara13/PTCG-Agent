
def meta_mm(a, b, out_dtype: torch.dtype | None = None):
    torch._check(a.dim() == 2, lambda: "a must be 2D")
    torch._check(b.dim() == 2, lambda: "b must be 2D")
    N, M1 = a.shape
    M2, P = b.shape
    torch._check(
        M1 == M2,
        lambda: f"a and b must have same reduction dim, but got [{N}, {M1}] X [{M2}, {P}].",
    )
    if out_dtype is not None:
        torch._check(
            out_dtype == a.dtype
            or (
                out_dtype == torch.float32
                and a.dtype in (torch.float16, torch.bfloat16)
            ),
            lambda: "out_dtype must be the same as input dtype or fp32 for fp16/bf16 inputs",
        )
    result_dtype = a.dtype if out_dtype is None else out_dtype
    return a.new_empty((N, P), dtype=result_dtype)

