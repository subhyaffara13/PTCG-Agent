
def get_fignums() -> list[int]:
    """Return a list of existing figure numbers."""
    return sorted(_pylab_helpers.Gcf.figs)

