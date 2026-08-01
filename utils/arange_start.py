
def arange_start(
    start: number, end: number, inp0: Any, inp1: Any, inp2: Any, inp3: Any
):
    if end < 0:
        raise AssertionError(f"Expected end ({end}) >= 0")
    if end < start:
        raise AssertionError(f"Expected end ({end}) >= start ({start})")
    return [int(math.ceil(end - start))]


def arange_start(
    start: NumberType,
    end: NumberType,
    *,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    device: torch.device | None = None,
    pin_memory: bool = False,
):
    return aten.arange.start_step(
        start, end, 1, dtype=dtype, layout=layout, device=device, pin_memory=pin_memory
    )

