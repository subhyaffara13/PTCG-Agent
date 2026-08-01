
def test_importing():
    from collections import OrderedDict

    from pybind11_tests.modules import OD

    assert OD is OrderedDict

