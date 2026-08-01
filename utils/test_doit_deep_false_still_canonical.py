
def test_doit_deep_false_still_canonical():
    assert (MatMul(C, Transpose(D*C), 2).doit(deep=False).args ==
            (2, C, Transpose(D*C)))

