
def test_numpy():
  try:
    import numpy as np
    y = np.array
    x = y([1,2,3])
    assert importable(x, source=False) == 'from numpy import array\narray([1, 2, 3])\n'
    assert importable(y, source=False) == 'from %s import array\n' % y.__module__
    assert importable(x, source=True) == 'from numpy import array\narray([1, 2, 3])\n'
    assert importable(y, source=True) == 'from %s import array\n' % y.__module__
    y = np.int64
    x = y(0)
    assert importable(x, source=False) == 'from numpy import int64\nint64(0)\n'
    assert importable(y, source=False) == 'from %s import int64\n' % y.__module__
    assert importable(x, source=True) == 'from numpy import int64\nint64(0)\n'
    assert importable(y, source=True) == 'from %s import int64\n' % y.__module__
    y = np.bool_
    x = y(0)
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=FutureWarning)
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        if hasattr(np, 'bool'): b = 'bool_' if np.bool is bool else 'bool'
        else: b = 'bool_'
    assert importable(x, source=False) == 'from numpy import %s\n%s(False)\n' % (b,b)
    assert importable(y, source=False) == 'from %s import %s\n' % (y.__module__,b)
    assert importable(x, source=True) == 'from numpy import %s\n%s(False)\n' % (b,b)
    assert importable(y, source=True) == 'from %s import %s\n' % (y.__module__,b)
  except ImportError: pass

