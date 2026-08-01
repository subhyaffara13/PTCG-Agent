
def test_max_min_non_numeric():
    # #2700
    aa = DataFrame({"nn": [11, 11, 22, 22], "ii": [1, 2, 3, 4], "ss": 4 * ["mama"]})

    result = aa.groupby("nn").max()
    assert "ss" in result

    result = aa.groupby("nn").max(numeric_only=False)
    assert "ss" in result

    result = aa.groupby("nn").min()
    assert "ss" in result

    result = aa.groupby("nn").min(numeric_only=False)
    assert "ss" in result

