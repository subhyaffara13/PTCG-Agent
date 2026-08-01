
def test_mixed_args_and_kwargs(msg):
    mpa = m.mixed_plus_args
    mpk = m.mixed_plus_kwargs
    mpak = m.mixed_plus_args_kwargs
    mpakd = m.mixed_plus_args_kwargs_defaults

    assert mpa(1, 2.5, 4, 99.5, None) == (1, 2.5, (4, 99.5, None))
    assert mpa(1, 2.5) == (1, 2.5, ())
    with pytest.raises(TypeError) as excinfo:
        assert mpa(1)
    assert (
        msg(excinfo.value)
        == """
        mixed_plus_args(): incompatible function arguments. The following argument types are supported:
            1. (arg0: int, arg1: float, *args) -> tuple

        Invoked with: 1
    """
    )
    with pytest.raises(TypeError) as excinfo:
        assert mpa()
    assert (
        msg(excinfo.value)
        == """
        mixed_plus_args(): incompatible function arguments. The following argument types are supported:
            1. (arg0: int, arg1: float, *args) -> tuple

        Invoked with:
    """
    )

    assert mpk(-2, 3.5, pi=3.14159, e=2.71828) == (
        -2,
        3.5,
        {"e": 2.71828, "pi": 3.14159},
    )
    assert mpak(7, 7.7, 7.77, 7.777, 7.7777, minusseven=-7) == (
        7,
        7.7,
        (7.77, 7.777, 7.7777),
        {"minusseven": -7},
    )
    assert mpakd() == (1, 3.14159, (), {})
    assert mpakd(3) == (3, 3.14159, (), {})
    assert mpakd(j=2.71828) == (1, 2.71828, (), {})
    assert mpakd(k=42) == (1, 3.14159, (), {"k": 42})
    assert mpakd(1, 1, 2, 3, 5, 8, then=13, followedby=21) == (
        1,
        1,
        (2, 3, 5, 8),
        {"then": 13, "followedby": 21},
    )
    # Arguments specified both positionally and via kwargs should fail:
    with pytest.raises(TypeError) as excinfo:
        assert mpakd(1, i=1)
    assert (
        msg(excinfo.value)
        == """
        mixed_plus_args_kwargs_defaults(): incompatible function arguments. The following argument types are supported:
            1. (i: int = 1, j: float = 3.14159, *args, **kwargs) -> tuple

        Invoked with: 1; kwargs: i=1
    """
    )
    with pytest.raises(TypeError) as excinfo:
        assert mpakd(1, 2, j=1)
    assert (
        msg(excinfo.value)
        == """
        mixed_plus_args_kwargs_defaults(): incompatible function arguments. The following argument types are supported:
            1. (i: int = 1, j: float = 3.14159, *args, **kwargs) -> tuple

        Invoked with: 1, 2; kwargs: j=1
    """
    )

    # Arguments after a py::args are automatically keyword-only (pybind 2.9+)
    assert m.args_kwonly(2, 2.5, z=22) == (2, 2.5, (), 22)
    assert m.args_kwonly(2, 2.5, "a", "b", "c", z=22) == (2, 2.5, ("a", "b", "c"), 22)
    assert m.args_kwonly(z=22, i=4, j=16) == (4, 16, (), 22)

    with pytest.raises(TypeError) as excinfo:
        assert m.args_kwonly(2, 2.5, 22)  # missing z= keyword
    assert (
        msg(excinfo.value)
        == """
        args_kwonly(): incompatible function arguments. The following argument types are supported:
            1. (i: int, j: float, *args, z: int) -> tuple

        Invoked with: 2, 2.5, 22
    """
    )

    assert m.args_kwonly_kwargs(i=1, k=4, j=10, z=-1, y=9) == (
        1,
        10,
        (),
        -1,
        {"k": 4, "y": 9},
    )
    assert m.args_kwonly_kwargs(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, z=11, y=12) == (
        1,
        2,
        (3, 4, 5, 6, 7, 8, 9, 10),
        11,
        {"y": 12},
    )
    assert (
        m.args_kwonly_kwargs.__doc__
        == "args_kwonly_kwargs(i: int, j: float, *args, z: int, **kwargs) -> tuple\n"
    )

    assert (
        m.args_kwonly_kwargs_defaults.__doc__
        == "args_kwonly_kwargs_defaults(i: int = 1, j: float = 3.14159, *args, z: int = 42, **kwargs) -> tuple\n"
    )
    assert m.args_kwonly_kwargs_defaults() == (1, 3.14159, (), 42, {})
    assert m.args_kwonly_kwargs_defaults(2) == (2, 3.14159, (), 42, {})
    assert m.args_kwonly_kwargs_defaults(z=-99) == (1, 3.14159, (), -99, {})
    assert m.args_kwonly_kwargs_defaults(5, 6, 7, 8) == (5, 6, (7, 8), 42, {})
    assert m.args_kwonly_kwargs_defaults(5, 6, 7, m=8) == (5, 6, (7,), 42, {"m": 8})
    assert m.args_kwonly_kwargs_defaults(5, 6, 7, m=8, z=9) == (5, 6, (7,), 9, {"m": 8})

