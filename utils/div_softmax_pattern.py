
def div_softmax_pattern(match: Match, *, inp, other, dim, keepdim, dtype=None):
    def repl(inp, other):
        if dtype is not None:
            inp = inp.to(dtype)

        sign: int | float | torch.Tensor
        if isinstance(other, (int, float, torch.SymInt, torch.SymFloat)):
            sign = 1 if other >= 0 else -1
        else:
            one = torch.scalar_tensor(1, dtype=inp.dtype, device=inp.device)
            sign = torch.where(other >= 0, one, -one)

        inp = inp * sign
        max_ = torch.amax(inp, dim=dim, keepdim=keepdim)

        return (inp - max_) / (sign * other)

    # pyrefly: ignore [bad-argument-type]
    match.replace_by_example(repl, [inp, other])

