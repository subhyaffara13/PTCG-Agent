
def _raise_if_figure_exists(num, func_name, clear=False):
    """
    Raise a ValueError if the figure *num* already exists.
    """
    if num is not None and not clear:
        if isinstance(num, FigureBase):
            raise ValueError(
                f"num {num!r} cannot be a FigureBase instance. "
                f"plt.{func_name}() is for creating new figures. "
                f"To add to an existing figure, use fig.{func_name}() "
                "instead.")

        if fignum_exists(num):
            raise ValueError(
                f"Figure {num!r} already exists. Use plt.figure({num!r}) "
                f"to get it or plt.close({num!r}) to close it. "
                f"Alternatively, pass 'clear=True' to {func_name}().")

