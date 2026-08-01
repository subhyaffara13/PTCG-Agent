
def test_type_errors():
    lp = _LPProblem(
        c=[1, 2],
        A_ub=np.array([[1, 1], [2, 2]]),
        b_ub=np.array([1, 1]),
        A_eq=np.array([[1, 1], [2, 2]]),
        b_eq=np.array([1, 1]),
        bounds=[(0, 1)]
    )
    bad = "hello"

    assert_raises(TypeError, _clean_inputs, lp._replace(c=bad))
    assert_raises(TypeError, _clean_inputs, lp._replace(A_ub=bad))
    assert_raises(TypeError, _clean_inputs, lp._replace(b_ub=bad))
    assert_raises(TypeError, _clean_inputs, lp._replace(A_eq=bad))
    assert_raises(TypeError, _clean_inputs, lp._replace(b_eq=bad))

    assert_raises(ValueError, _clean_inputs, lp._replace(bounds=bad))
    assert_raises(ValueError, _clean_inputs, lp._replace(bounds="hi"))
    assert_raises(ValueError, _clean_inputs, lp._replace(bounds=["hi"]))
    assert_raises(ValueError, _clean_inputs, lp._replace(bounds=[("hi")]))
    assert_raises(ValueError, _clean_inputs, lp._replace(bounds=[(1, "")]))
    assert_raises(ValueError, _clean_inputs, lp._replace(bounds=[(1, 2), (1, "")]))
    assert_raises(TypeError, _clean_inputs,
                  lp._replace(bounds=[(1, date(2020, 2, 29))]))
    assert_raises(ValueError, _clean_inputs, lp._replace(bounds=[[[1, 2]]]))


def test_type_errors() -> None:
    # subscripts must be a string
    with pytest.raises(TypeError):
        contract(0, 0)

    # out parameter must be an array
    with pytest.raises(TypeError):
        contract("", 0, out="test")

    # order parameter must be a valid order
    # changed in Numpy 1.19, see https://github.com/numpy/numpy/commit/35b0a051c19265f5643f6011ee11e31d30c8bc4c
    with pytest.raises((TypeError, ValueError)):
        contract("", 0, order="W")  # type: ignore

    # casting parameter must be a valid casting
    with pytest.raises(ValueError):
        contract("", 0, casting="blah")  # type: ignore

    # dtype parameter must be a valid dtype
    with pytest.raises(TypeError):
        contract("", 0, dtype="bad_data_type")

    # other keyword arguments are rejected
    with pytest.raises(TypeError):
        contract("", 0, bad_arg=0)

    # issue 4528 revealed a segfault with this call
    with pytest.raises(TypeError):
        contract(*(None,) * 63)

    # Cannot have two ->
    with pytest.raises(ValueError):
        contract("->,->", 0, 5)

    # Undefined symbol lhs
    with pytest.raises(ValueError):
        contract("&,a->", 0, 5)

    # Undefined symbol rhs
    with pytest.raises(ValueError):
        contract("a,a->&", 0, 5)

    with pytest.raises(ValueError):
        contract("a,a->&", 0, 5)

    # Catch ellipsis errors
    string = "...a->...a"
    views = build_views(string)

    # Subscript list must contain Ellipsis or (hashable && comparable) object
    with pytest.raises(TypeError):
        contract(views[0], [Ellipsis, 0], [Ellipsis, ["a"]])

    with pytest.raises(TypeError):
        contract(views[0], [Ellipsis, {}], [Ellipsis, "a"])

