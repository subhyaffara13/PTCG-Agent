
def test_nat_comparisons_invalid(other_and_type, symbol_and_op):
    # GH#35585
    other, other_type = other_and_type
    symbol, op = symbol_and_op

    assert not NaT == other
    assert not other == NaT

    assert NaT != other
    assert other != NaT

    msg = f"'{symbol}' not supported between instances of 'NaTType' and '{other_type}'"
    with pytest.raises(TypeError, match=msg):
        op(NaT, other)

    msg = f"'{symbol}' not supported between instances of '{other_type}' and 'NaTType'"
    with pytest.raises(TypeError, match=msg):
        op(other, NaT)

