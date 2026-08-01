
def test_uses_pandas_na():
    a = pd.array([1, None], dtype=Float64Dtype())
    assert a[1] is pd.NA


def test_uses_pandas_na():
    a = pd.array([1, None], dtype=Int64Dtype())
    assert a[1] is pd.NA

