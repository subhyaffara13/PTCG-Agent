
def test_get_accessor_args():
    func = plotting._core.PlotAccessor._get_call_args

    msg = "Called plot accessor for type list, expected Series or DataFrame"
    with pytest.raises(TypeError, match=msg):
        func(backend_name="", data=[], args=[], kwargs={})

    msg = "should not be called with positional arguments"
    with pytest.raises(TypeError, match=msg):
        func(backend_name="", data=Series(dtype=object), args=["line", None], kwargs={})

    x, y, kind, kwargs = func(
        backend_name="",
        data=DataFrame(),
        args=["x"],
        kwargs={"y": "y", "kind": "bar", "grid": False},
    )
    assert x == "x"
    assert y == "y"
    assert kind == "bar"
    assert kwargs == {"grid": False}

    x, y, kind, kwargs = func(
        backend_name="pandas.plotting._matplotlib",
        data=Series(dtype=object),
        args=[],
        kwargs={},
    )
    assert x is None
    assert y is None
    assert kind == "line"
    assert len(kwargs) == 24

