import sys

def test__mem_available():
    # May return None on non-Linux platforms
    available = _get_mem_available()
    if sys.platform.startswith('linux'):
        assert available >= 0
    else:
        assert available is None or available >= 0

