
def get_layout_engine(fig: Figure) -> mpl.layout_engine.LayoutEngine | None:
    """Handle changes to auto layout engine interface in 3.6"""
    if hasattr(fig, "get_layout_engine"):
        return fig.get_layout_engine()
    else:
        # _version_predates(mpl, 3.6)
        return None

