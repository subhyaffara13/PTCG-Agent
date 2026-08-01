
def test_error_invalid_object(data, all_arithmetic_operators):
    data, _ = data

    op = all_arithmetic_operators
    opa = getattr(data, op)

    # 2d -> return NotImplemented
    result = opa(pd.DataFrame({"A": data}))
    assert result is NotImplemented

    msg = r"can only perform ops with 1-d structures"
    with pytest.raises(NotImplementedError, match=msg):
        opa(np.arange(len(data)).reshape(-1, len(data)))

