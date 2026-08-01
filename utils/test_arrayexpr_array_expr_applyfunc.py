
def test_arrayexpr_array_expr_applyfunc():

    A = ArraySymbol("A", (3, k, 2))
    aaf = ArrayElementwiseApplyFunc(sin, A)
    assert aaf.shape == (3, k, 2)

