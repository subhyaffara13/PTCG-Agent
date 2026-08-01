
def stem(
    *args: ArrayLike | str,
    linefmt: str | None = None,
    markerfmt: str | None = None,
    basefmt: str | None = None,
    bottom: float = 0,
    label: str | None = None,
    orientation: Literal["vertical", "horizontal"] = "vertical",
    data: DataParamType = None,
) -> StemContainer:
    return gca().stem(
        *args,
        linefmt=linefmt,
        markerfmt=markerfmt,
        basefmt=basefmt,
        bottom=bottom,
        label=label,
        orientation=orientation,
        **({"data": data} if data is not None else {}),
    )

