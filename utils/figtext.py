
def figtext(
    x: float, y: float, s: str, fontdict: dict[str, Any] | None = None, **kwargs
) -> Text:
    return gcf().text(x, y, s, fontdict=fontdict, **kwargs)

