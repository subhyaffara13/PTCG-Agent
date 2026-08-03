from typing import Any

def xlabel(
    xlabel: str,
    fontdict: dict[str, Any] | None = None,
    labelpad: float | None = None,
    *,
    loc: Literal["left", "center", "right"] | None = None,
    **kwargs,
) -> Text:
    return gca().set_xlabel(
        xlabel, fontdict=fontdict, labelpad=labelpad, loc=loc, **kwargs
    )

