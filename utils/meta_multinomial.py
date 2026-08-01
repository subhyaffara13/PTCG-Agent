
def meta_multinomial(input, num_samples, replacement=False, *, generator=None):
    torch._check(
        0 < input.dim() <= 2,
        lambda: f"The probability distributions dimensions must be 1 or 2, but got {input.dim()}",
    )
    if input.dim() == 1:
        return torch.empty(num_samples, dtype=torch.long, device=input.device)
    return torch.empty(
        input.size(0), num_samples, dtype=torch.long, device=input.device
    )

