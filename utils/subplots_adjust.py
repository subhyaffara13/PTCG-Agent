
def subplots_adjust(
    left: float | None = None,
    bottom: float | None = None,
    right: float | None = None,
    top: float | None = None,
    wspace: float | None = None,
    hspace: float | None = None,
) -> None:
    gcf().subplots_adjust(
        left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace
    )

