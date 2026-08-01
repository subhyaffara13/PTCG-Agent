
def test_missing_column(method, func):
    # GH 40004
    obj = DataFrame({"A": [1]})
    msg = r"Label\(s\) \['B'\] do not exist"
    with pytest.raises(KeyError, match=msg):
        getattr(obj, method)(func)

