
def _uniform_random_(t: torch.Tensor, low: float, high: float) -> torch.Tensor:
    # uniform_ requires to-from <= std::numeric_limits<scalar_t>::max()
    # Work around this by scaling the range before and after the PRNG
    if high - low >= torch.finfo(t.dtype).max:
        return t.uniform_(low / 2, high / 2).mul_(2)
    else:
        return t.uniform_(low, high)

