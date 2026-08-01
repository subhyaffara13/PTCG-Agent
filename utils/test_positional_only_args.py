
def test_positional_only_args():
    assert m.pos_only_all(1, 2) == (1, 2)
    assert m.pos_only_all(2, 1) == (2, 1)

    with pytest.raises(TypeError) as excinfo:
        m.pos_only_all(i=1, j=2)
    assert "incompatible function arguments" in str(excinfo.value)

    assert m.pos_only_mix(1, 2) == (1, 2)
    assert m.pos_only_mix(2, j=1) == (2, 1)

    with pytest.raises(TypeError) as excinfo:
        m.pos_only_mix(i=1, j=2)
    assert "incompatible function arguments" in str(excinfo.value)

    assert m.pos_kw_only_mix(1, 2, k=3) == (1, 2, 3)
    assert m.pos_kw_only_mix(1, j=2, k=3) == (1, 2, 3)

    with pytest.raises(TypeError) as excinfo:
        m.pos_kw_only_mix(i=1, j=2, k=3)
    assert "incompatible function arguments" in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        m.pos_kw_only_mix(1, 2, 3)
    assert "incompatible function arguments" in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        m.pos_only_def_mix()
    assert "incompatible function arguments" in str(excinfo.value)

    assert m.pos_only_def_mix(1) == (1, 2, 3)
    assert m.pos_only_def_mix(1, 4) == (1, 4, 3)
    assert m.pos_only_def_mix(1, 4, 7) == (1, 4, 7)
    assert m.pos_only_def_mix(1, 4, k=7) == (1, 4, 7)

    with pytest.raises(TypeError) as excinfo:
        m.pos_only_def_mix(1, j=4)
    assert "incompatible function arguments" in str(excinfo.value)

    # Mix it with args and kwargs:
    assert (
        m.args_kwonly_full_monty.__doc__
        == "args_kwonly_full_monty(arg0: int = 1, arg1: int = 2, /, j: float = 3.14159, *args, z: int = 42, **kwargs) -> tuple\n"
    )
    assert m.args_kwonly_full_monty() == (1, 2, 3.14159, (), 42, {})
    assert m.args_kwonly_full_monty(8) == (8, 2, 3.14159, (), 42, {})
    assert m.args_kwonly_full_monty(8, 9) == (8, 9, 3.14159, (), 42, {})
    assert m.args_kwonly_full_monty(8, 9, 10) == (8, 9, 10.0, (), 42, {})
    assert m.args_kwonly_full_monty(3, 4, 5, 6, 7, m=8, z=9) == (
        3,
        4,
        5.0,
        (
            6,
            7,
        ),
        9,
        {"m": 8},
    )
    assert m.args_kwonly_full_monty(3, 4, 5, 6, 7, m=8, z=9) == (
        3,
        4,
        5.0,
        (
            6,
            7,
        ),
        9,
        {"m": 8},
    )
    assert m.args_kwonly_full_monty(5, j=7, m=8, z=9) == (5, 2, 7.0, (), 9, {"m": 8})
    assert m.args_kwonly_full_monty(i=5, j=7, m=8, z=9) == (
        1,
        2,
        7.0,
        (),
        9,
        {"i": 5, "m": 8},
    )

    # pos_only at the beginning of the argument list was "broken" in how it was displayed (though
    # this is fairly useless in practice).  Related to:
    # https://github.com/pybind/pybind11/pull/3402#issuecomment-963341987
    assert (
        m.first_arg_kw_only.pos_only.__doc__
        == "pos_only(self: pybind11_tests.kwargs_and_defaults.first_arg_kw_only, /, i: int, j: int) -> None\n"
    )

