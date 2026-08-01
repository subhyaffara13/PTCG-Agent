
def ylabel(
    ylabel: str,
    fontdict: dict[str, Any] | None = None,
    labelpad: float | None = None,
    *,
    loc: Literal["bottom", "center", "top"] | None = None,
    **kwargs,
) -> Text:
    return gca().set_ylabel(
        ylabel, fontdict=fontdict, labelpad=labelpad, loc=loc, **kwargs
    )

