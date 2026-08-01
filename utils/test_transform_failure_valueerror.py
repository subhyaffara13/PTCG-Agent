
def test_transform_failure_valueerror():
    # GH 40211
    def op(x):
        if np.sum(np.sum(x)) < 10:
            raise ValueError
        return x

    df = DataFrame({"A": [1, 2, 3], "B": [400, 500, 600]})
    msg = "Transform function failed"

    with pytest.raises(ValueError, match=msg):
        df.transform([op])

    with pytest.raises(ValueError, match=msg):
        df.transform({"A": op, "B": op})

    with pytest.raises(ValueError, match=msg):
        df.transform({"A": [op], "B": [op]})

    with pytest.raises(ValueError, match=msg):
        df.transform({"A": [op, "shift"], "B": [op]})

