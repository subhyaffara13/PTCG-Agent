
def _restore_foreground_window_at_end():
    foreground = _c_internal_utils.Win32_GetForegroundWindow()
    try:
        yield
    finally:
        if foreground and mpl.rcParams['tk.window_focus']:
            _c_internal_utils.Win32_SetForegroundWindow(foreground)

