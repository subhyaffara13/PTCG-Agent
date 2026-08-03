import os

def savefig(fname: str | os.PathLike | IO, **kwargs) -> None:
    fig = gcf()
    # savefig default implementation has no return, so mypy is unhappy
    # presumably this is here because subclasses can return?
    res = fig.savefig(fname, **kwargs)  # type: ignore[func-returns-value]
    fig.canvas.draw_idle()  # Need this if 'transparent=True', to reset colors.
    return res

