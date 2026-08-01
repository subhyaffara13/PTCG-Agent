
def test_named_arguments():
    a = np.array([[1.0, 2], [3, 4], [5, 6]])
    b = np.ones((2, 1))

    assert np.all(m.matrix_multiply(a, b) == np.array([[3.0], [7], [11]]))
    assert np.all(m.matrix_multiply(A=a, B=b) == np.array([[3.0], [7], [11]]))
    assert np.all(m.matrix_multiply(B=b, A=a) == np.array([[3.0], [7], [11]]))

    with pytest.raises(ValueError) as excinfo:
        m.matrix_multiply(b, a)
    assert str(excinfo.value) == "Nonconformable matrices!"

    with pytest.raises(ValueError) as excinfo:
        m.matrix_multiply(A=b, B=a)
    assert str(excinfo.value) == "Nonconformable matrices!"

    with pytest.raises(ValueError) as excinfo:
        m.matrix_multiply(B=a, A=b)
    assert str(excinfo.value) == "Nonconformable matrices!"


def test_named_arguments():
    assert m.kw_func0(5, 10) == "x=5, y=10"

    assert m.kw_func1(5, 10) == "x=5, y=10"
    assert m.kw_func1(5, y=10) == "x=5, y=10"
    assert m.kw_func1(y=10, x=5) == "x=5, y=10"

    assert m.kw_func2() == "x=100, y=200"
    assert m.kw_func2(5) == "x=5, y=200"
    assert m.kw_func2(x=5) == "x=5, y=200"
    assert m.kw_func2(y=10) == "x=100, y=10"
    assert m.kw_func2(5, 10) == "x=5, y=10"
    assert m.kw_func2(x=5, y=10) == "x=5, y=10"

    with pytest.raises(TypeError) as excinfo:
        # noinspection PyArgumentList
        m.kw_func2(x=5, y=10, z=12)
    assert excinfo.match(
        r"(?s)^kw_func2\(\): incompatible.*Invoked with: kwargs: ((x=5|y=10|z=12)(, |$)){3}$"
    )

    assert m.kw_func4() == "{13 17}"
    assert m.kw_func4(myList=[1, 2, 3]) == "{1 2 3}"

    assert m.kw_func_udl(x=5, y=10) == "x=5, y=10"
    assert m.kw_func_udl_z(x=5) == "x=5, y=0"

