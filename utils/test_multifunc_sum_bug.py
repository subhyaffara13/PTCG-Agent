
def test_multifunc_sum_bug():
    # GH #1065
    x = DataFrame(np.arange(9).reshape(3, 3))
    x["test"] = 0
    x["fl"] = [1.3, 1.5, 1.6]

    grouped = x.groupby("test")
    result = grouped.agg({"fl": "sum", 2: "size"})
    assert result["fl"].dtype == np.float64

