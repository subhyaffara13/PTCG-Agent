
def test_compat():
    # test we have compat with our version of numexpr

    from pandas.core.computation.check import NUMEXPR_INSTALLED

    ne = pytest.importorskip("numexpr")

    ver = ne.__version__
    if Version(ver) < Version(VERSIONS["numexpr"]):
        assert not NUMEXPR_INSTALLED
    else:
        assert NUMEXPR_INSTALLED

