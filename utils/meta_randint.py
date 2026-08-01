
def meta_randint(
    high,
    size,
    *,
    dtype=torch.long,
    layout=None,
    device=None,
    pin_memory=None,
):
    low = 0
    torch._check(
        high > low,
        lambda: f"random_ expects 'from' to be less than 'to', but got from={low} >= to={high}",
    )
    return torch.empty(
        size, dtype=dtype, layout=layout, device=device, pin_memory=pin_memory
    )

