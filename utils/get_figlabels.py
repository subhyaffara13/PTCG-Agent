from typing import Any

def get_figlabels() -> list[Any]:
    """Return a list of existing figure labels."""
    managers = _pylab_helpers.Gcf.get_all_fig_managers()
    managers.sort(key=lambda m: m.num)
    return [m.canvas.figure.get_label() for m in managers]

