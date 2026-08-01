
def tick_params(axis: Literal["both", "x", "y"] = "both", **kwargs) -> None:
    gca().tick_params(axis=axis, **kwargs)

