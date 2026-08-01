
def test_nat_comparisons(compare_operators_no_eq_ne, other):
    # GH 26039
    opname = compare_operators_no_eq_ne

    assert getattr(NaT, opname)(other) is False

    op = getattr(operator, opname.strip("_"))
    assert op(NaT, other) is False
    assert op(other, NaT) is False

