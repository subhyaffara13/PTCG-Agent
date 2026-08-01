
def ticklabel_format(
    *,
    axis: Literal["both", "x", "y"] = "both",
    style: Literal["", "sci", "scientific", "plain"] | None = None,
    scilimits: tuple[int, int] | None = None,
    useOffset: bool | float | None = None,
    useLocale: bool | None = None,
    useMathText: bool | None = None,
) -> None:
    gca().ticklabel_format(
        axis=axis,
        style=style,
        scilimits=scilimits,
        useOffset=useOffset,
        useLocale=useLocale,
        useMathText=useMathText,
    )

