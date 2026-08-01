
def set_pyqt_clipboard(monkeypatch):
    qt_cut, qt_paste = init_qt_clipboard()
    with monkeypatch.context() as m:
        m.setattr(pd.io.clipboard, "clipboard_set", qt_cut)
        m.setattr(pd.io.clipboard, "clipboard_get", qt_paste)
        yield

