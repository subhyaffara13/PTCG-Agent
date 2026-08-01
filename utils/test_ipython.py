
def test_ipython():
    from matplotlib.testing import ipython_in_subprocess
    ipython_in_subprocess("osx", {(8, 24): "macosx", (7, 0): "MacOSX"})


def test_ipython():
    from matplotlib.testing import ipython_in_subprocess
    ipython_in_subprocess("qt", {(8, 24): "qtagg", (8, 15): "QtAgg", (7, 0): "Qt5Agg"})

