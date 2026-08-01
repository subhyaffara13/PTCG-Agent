
def _collect_new_figures():
    """
    After::

        with _collect_new_figures() as figs:
            some_code()

    the list *figs* contains the figures that have been created during the
    execution of ``some_code``, sorted by figure number.
    """
    managers = _pylab_helpers.Gcf.figs
    preexisting = [manager for manager in managers.values()]
    new_figs = []
    try:
        yield new_figs
    finally:
        new_managers = sorted([manager for manager in managers.values()
                               if manager not in preexisting],
                              key=lambda manager: manager.num)
        new_figs[:] = [manager.canvas.figure for manager in new_managers]

