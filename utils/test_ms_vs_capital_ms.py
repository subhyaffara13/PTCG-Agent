
def test_ms_vs_capital_ms():
    left = _get_offset("ms")
    right = _get_offset("MS")

    assert left == offsets.Milli()
    assert right == offsets.MonthBegin()

