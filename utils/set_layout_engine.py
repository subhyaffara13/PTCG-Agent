
def set_layout_engine(
    fig: Figure,
    engine: Literal["constrained", "compressed", "tight", "none"],
) -> None:
    """Handle changes to auto layout engine interface in 3.6"""
    if hasattr(fig, "set_layout_engine"):
        fig.set_layout_engine(engine)
    else:
        # _version_predates(mpl, 3.6)
        if engine == "tight":
            fig.set_tight_layout(True)  # type: ignore  # predates typing
        elif engine == "constrained":
            fig.set_constrained_layout(True)  # type: ignore
        elif engine == "none":
            fig.set_tight_layout(False)  # type: ignore
            fig.set_constrained_layout(False)  # type: ignore

