
def trim_sigfig(x: float, n: int) -> float:
    """Trim `x` to `n` significant figures. (e.g. 3.14159, 2 -> 3.10000)"""
    if n != int(n):
        raise AssertionError("Number of significant figures must be an integer")
    magnitude = int(torch.tensor(x).abs().log10().ceil().item())
    scale = 10 ** (magnitude - n)
    return float(torch.tensor(x / scale).round() * scale)

