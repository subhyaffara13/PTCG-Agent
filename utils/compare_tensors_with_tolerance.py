
def compare_tensors_with_tolerance(
    name: str,
    tensor1: torch.Tensor,
    tensor2: torch.Tensor,
    atol=5e-3,
    rtol=1e-4,
    mismatch_percentage_tolerance=0.1,
) -> bool:
    assert tensor1.shape == tensor2.shape
    a = tensor1.clone().float()
    b = tensor2.clone().float()

    differences = torch.abs(a - b)
    mismatch_count = (differences > (rtol * torch.max(torch.abs(a), torch.abs(b)) + atol)).sum().item()

    total_elements = a.numel()
    mismatch_percentage = (mismatch_count / total_elements) * 100

    passed = mismatch_percentage < mismatch_percentage_tolerance

    log_func = logger.error if not passed else logger.info
    log_func(
        "%s: mismatched elements percentage %.2f (%d/%d). Verification %s (threshold=%.2f).",
        name,
        mismatch_percentage,
        mismatch_count,
        total_elements,
        "passed" if passed else "failed",
        mismatch_percentage_tolerance,
    )

    return passed

