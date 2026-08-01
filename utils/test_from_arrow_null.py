
def test_from_arrow_null(data, arr):
    res = data.dtype.__from_arrow__(arr)
    assert res.isna().all()
    assert len(res) == 10

