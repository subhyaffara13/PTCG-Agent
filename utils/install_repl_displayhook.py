import sys

def install_repl_displayhook() -> None:
    """
    Connect to the display hook of the current shell.

    The display hook gets called when the read-evaluate-print-loop (REPL) of
    the shell has finished the execution of a command. We use this callback
    to be able to automatically update a figure in interactive mode.

    This works both with IPython and with vanilla python shells.
    """
    global _REPL_DISPLAYHOOK

    if _REPL_DISPLAYHOOK is _ReplDisplayHook.IPYTHON:
        return

    # See if we have IPython hooks around, if so use them.
    # Use ``sys.modules.get(name)`` rather than ``name in sys.modules`` as
    # entries can also have been explicitly set to None.
    mod_ipython = sys.modules.get("IPython")
    if not mod_ipython:
        _REPL_DISPLAYHOOK = _ReplDisplayHook.PLAIN
        return
    ip = mod_ipython.get_ipython()
    if not ip:
        _REPL_DISPLAYHOOK = _ReplDisplayHook.PLAIN
        return

    ip.events.register("post_execute", _draw_all_if_interactive)
    _REPL_DISPLAYHOOK = _ReplDisplayHook.IPYTHON

    if mod_ipython.version_info[:2] < (8, 24):
        # Use of backend2gui is not needed for IPython >= 8.24 as that functionality
        # has been moved to Matplotlib.
        # This code can be removed when Python 3.12, the latest version supported by
        # IPython < 8.24, reaches end-of-life in late 2028.
        from IPython.core.pylabtools import backend2gui
        ipython_gui_name = backend2gui.get(get_backend())
    else:
        _, ipython_gui_name = backend_registry.resolve_backend(get_backend())
    # trigger IPython's eventloop integration, if available
    if ipython_gui_name:
        ip.enable_gui(ipython_gui_name)

