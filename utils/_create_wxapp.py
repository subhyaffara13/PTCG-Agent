
def _create_wxapp():
    wxapp = wx.App(False)
    wxapp.SetExitOnFrameDelete(True)
    cbook._setup_new_guiapp()
    # Set per-process DPI awareness. This is a NoOp except in MSW
    _c_internal_utils.Win32_SetProcessDpiAwareness_max()
    return wxapp

