
def test_apply_categorical_func():
    # GH 9573
    df = DataFrame({"c0": ["A", "A", "B", "B"], "c1": ["C", "C", "D", "D"]})
    result = df.apply(lambda ts: ts.astype("category"))

    assert result.shape == (4, 2)
    assert isinstance(result["c0"].dtype, CategoricalDtype)
    assert isinstance(result["c1"].dtype, CategoricalDtype)

