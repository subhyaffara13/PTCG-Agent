
def qt5_and_qt6_pairs():
    qt5_bindings = [
        dep for dep in ['PyQt5', 'PySide2']
        if importlib.util.find_spec(dep) is not None
    ]
    qt6_bindings = [
        dep for dep in ['PyQt6', 'PySide6']
        if importlib.util.find_spec(dep) is not None
    ]
    if len(qt5_bindings) == 0 or len(qt6_bindings) == 0:
        yield pytest.param(None, None,
                           marks=[pytest.mark.skip('need both QT6 and QT5 bindings')])
        return

    for qt5 in qt5_bindings:
        for qt6 in qt6_bindings:
            yield from ([qt5, qt6], [qt6, qt5])

