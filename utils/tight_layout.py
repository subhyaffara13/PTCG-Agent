
def tight_layout(
    *,
    pad: float = 1.08,
    h_pad: float | None = None,
    w_pad: float | None = None,
    rect: tuple[float, float, float, float] | None = None,
) -> None:
    gcf().tight_layout(pad=pad, h_pad=h_pad, w_pad=w_pad, rect=rect)

