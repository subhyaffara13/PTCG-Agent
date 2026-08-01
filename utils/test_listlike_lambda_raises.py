
def test_listlike_lambda_raises(ops):
    # GH53601
    df = DataFrame({"a": [1, 2]})
    with pytest.raises(ValueError, match="by_row=True not allowed"):
        df.apply(ops, by_row=True)

