
def meta_isin(elements, test_elements, *, assume_unique=False, invert=False):
    torch._check(
        isinstance(elements, Tensor) or isinstance(test_elements, Tensor),
        lambda: "At least one of elements and test_elements must be a Tensor.",
    )
    if not isinstance(elements, Tensor):
        elements = torch.tensor(elements, device=test_elements.device)

    if not isinstance(test_elements, Tensor):
        test_elements = torch.tensor(test_elements, device=elements.device)

    _check_for_unsupported_isin_dtype(elements.dtype)
    _check_for_unsupported_isin_dtype(test_elements.dtype)
    return torch.empty_like(elements, dtype=torch.bool)

