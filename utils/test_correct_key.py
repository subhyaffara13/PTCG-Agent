
def test_correct_key(backend, qt_key, qt_mods, answer, monkeypatch):
    """
    Make a figure.
    Send a key_press_event event (using non-public, qtX backend specific api).
    Catch the event.
    Assert sent and caught keys are the same.
    """
    from matplotlib.backends.qt_compat import _to_int, QtCore

    if sys.platform == "darwin" and answer is not None:
        answer = answer.replace("ctrl", "cmd")
        answer = answer.replace("control", "cmd")
        answer = answer.replace("meta", "ctrl")
    result = None
    qt_mod = QtCore.Qt.KeyboardModifier.NoModifier
    for mod in qt_mods:
        qt_mod |= getattr(QtCore.Qt.KeyboardModifier, mod)

    class _Event:
        def isAutoRepeat(self): return False
        def key(self): return _to_int(getattr(QtCore.Qt.Key, qt_key))

    monkeypatch.setattr(QtWidgets.QApplication, "keyboardModifiers",
                        lambda self: qt_mod)

    def on_key_press(event):
        nonlocal result
        result = event.key

    qt_canvas = plt.figure().canvas
    qt_canvas.mpl_connect('key_press_event', on_key_press)
    qt_canvas.keyPressEvent(_Event())
    assert result == answer

