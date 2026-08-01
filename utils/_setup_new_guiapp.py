
def _setup_new_guiapp():
    """
    Perform OS-dependent setup when Matplotlib creates a new GUI application.
    """
    # Windows: If not explicit app user model id has been set yet (so we're not
    # already embedded), then set it to "matplotlib", so that taskbar icons are
    # correct.
    try:
        _c_internal_utils.Win32_GetCurrentProcessExplicitAppUserModelID()
    except OSError:
        _c_internal_utils.Win32_SetCurrentProcessExplicitAppUserModelID(
            "matplotlib")

