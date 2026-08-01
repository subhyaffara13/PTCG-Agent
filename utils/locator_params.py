
def locator_params(
    axis: Literal["both", "x", "y"] = "both", tight: bool | None = None, **kwargs
) -> None:
    gca().locator_params(axis=axis, tight=tight, **kwargs)

