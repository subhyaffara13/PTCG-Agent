
def test_arrow_extension_type():
    pa = pytest.importorskip("pyarrow")

    from pandas.core.arrays.arrow.extension_types import ArrowIntervalType

    p1 = ArrowIntervalType(pa.int64(), "left")
    p2 = ArrowIntervalType(pa.int64(), "left")
    p3 = ArrowIntervalType(pa.int64(), "right")

    assert p1.closed == "left"
    assert p1 == p2
    assert p1 != p3
    assert hash(p1) == hash(p2)
    assert hash(p1) != hash(p3)


def test_arrow_extension_type():
    from pandas.core.arrays.arrow.extension_types import ArrowPeriodType

    p1 = ArrowPeriodType("D")
    p2 = ArrowPeriodType("D")
    p3 = ArrowPeriodType("M")

    assert p1.freq == "D"
    assert p1 == p2
    assert p1 != p3
    assert hash(p1) == hash(p2)
    assert hash(p1) != hash(p3)

