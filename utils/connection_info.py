
def connection_info():
    """
    Return a string showing the figure and connection status for the backend.

    This is intended as a diagnostic tool, and not for general use.
    """
    result = [
        '{fig} - {socket}'.format(
            fig=(manager.canvas.figure.get_label()
                 or f"Figure {manager.num}"),
            socket=manager.web_sockets)
        for manager in Gcf.get_all_fig_managers()
    ]
    if not is_interactive():
        result.append(f'Figures pending show: {len(Gcf.figs)}')
    return '\n'.join(result)

