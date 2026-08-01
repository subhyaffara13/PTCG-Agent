
def _check_for_unsupported_isin_dtype(dtype):
    torch._check(
        dtype not in (torch.bool, torch.complex128, torch.complex64),
        lambda: f"Unsupported input type encountered for isin(): {dtype}",
    )

