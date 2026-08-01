
def bar_label(
    container: BarContainer,
    labels: ArrayLike | None = None,
    *,
    fmt: str | Callable[[float], str] = "%g",
    label_type: Literal["center", "edge"] = "edge",
    padding: float | ArrayLike = 0,
    **kwargs,
) -> list[Annotation]:
    return gca().bar_label(
        container,
        labels=labels,
        fmt=fmt,
        label_type=label_type,
        padding=padding,
        **kwargs,
    )

