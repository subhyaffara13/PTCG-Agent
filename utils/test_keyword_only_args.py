
def test_keyword_only_args(msg):
    assert m.kw_only_all(i=1, j=2) == (1, 2)
    assert m.kw_only_all(j=1, i=2) == (2, 1)

    with pytest.raises(TypeError) as excinfo:
        assert m.kw_only_all(i=1) == (1,)
    assert "incompatible function arguments" in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        assert m.kw_only_all(1, 2) == (1, 2)
    assert "incompatible function arguments" in str(excinfo.value)

    assert m.kw_only_some(1, k=3, j=2) == (1, 2, 3)

    assert m.kw_only_with_defaults(z=8) == (3, 4, 5, 8)
    assert m.kw_only_with_defaults(2, z=8) == (2, 4, 5, 8)
    assert m.kw_only_with_defaults(2, j=7, k=8, z=9) == (2, 7, 8, 9)
    assert m.kw_only_with_defaults(2, 7, z=9, k=8) == (2, 7, 8, 9)

    assert m.kw_only_mixed(1, j=2) == (1, 2)
    assert m.kw_only_mixed(j=2, i=3) == (3, 2)
    assert m.kw_only_mixed(i=2, j=3) == (2, 3)

    assert m.kw_only_plus_more(4, 5, k=6, extra=7) == (4, 5, 6, {"extra": 7})
    assert m.kw_only_plus_more(3, k=5, j=4, extra=6) == (3, 4, 5, {"extra": 6})
    assert m.kw_only_plus_more(2, k=3, extra=4) == (2, -1, 3, {"extra": 4})

    with pytest.raises(TypeError) as excinfo:
        assert m.kw_only_mixed(i=1) == (1,)
    assert "incompatible function arguments" in str(excinfo.value)

    with pytest.raises(RuntimeError) as excinfo:
        m.register_invalid_kw_only(m)
    assert (
        msg(excinfo.value)
        == """
        arg(): cannot specify an unnamed argument after a kw_only() annotation or args() argument
    """
    )

    # https://github.com/pybind/pybind11/pull/3402#issuecomment-963341987
    x = m.first_arg_kw_only(i=1)
    x.method()
    x.method(i=1, j=2)
    assert (
        m.first_arg_kw_only.__init__.__doc__
        == "__init__(self: pybind11_tests.kwargs_and_defaults.first_arg_kw_only, *, i: int = 0) -> None\n"
    )
    assert (
        m.first_arg_kw_only.method.__doc__
        == "method(self: pybind11_tests.kwargs_and_defaults.first_arg_kw_only, *, i: int = 1, j: int = 2) -> None\n"
    )

