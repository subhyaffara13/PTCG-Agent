
def get_plot_commands() -> list[str]:
    """
    Get a sorted list of all of the plotting commands.
    """
    NON_PLOT_COMMANDS = {
        'connect', 'disconnect', 'get_current_fig_manager', 'ginput',
        'new_figure_manager', 'waitforbuttonpress'}
    return [name for name in _get_pyplot_commands()
            if name not in NON_PLOT_COMMANDS]

