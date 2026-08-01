
def get_current_fig_manager() -> FigureManagerBase | None:
    """
    Return the figure manager of the current figure.

    The figure manager is a container for the actual backend-depended window
    that displays the figure on screen.

    If no current figure exists, a new one is created, and its figure
    manager is returned.

    Returns
    -------
    `.FigureManagerBase` or backend-dependent subclass thereof
    """
    return gcf().canvas.manager

