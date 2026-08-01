
def ip():
    """
    Get an instance of IPython.InteractiveShell.

    Will raise a skip if IPython is not installed.
    """
    pytest.importorskip("IPython", minversion="6.0.0")
    from IPython.core.interactiveshell import InteractiveShell

    # GH#35711 make sure sqlite history file handle is not leaked
    from traitlets.config import Config  # isort:skip

    c = Config()
    c.HistoryManager.hist_file = ":memory:"

    return InteractiveShell(config=c)

