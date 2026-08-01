
def autoscale(
    enable: bool = True,
    axis: Literal["both", "x", "y"] = "both",
    tight: bool | None = None,
) -> None:
    gca().autoscale(enable=enable, axis=axis, tight=tight)

