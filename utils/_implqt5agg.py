
def _implqt5agg():
    import matplotlib.backends.backend_qt5agg  # noqa
    import sys

    assert 'PyQt6' not in sys.modules
    assert 'pyside6' not in sys.modules
    assert 'PyQt5' in sys.modules or 'pyside2' in sys.modules

