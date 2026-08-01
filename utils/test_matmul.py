
def test_matmul():
    a = Matrix([[1, 2], [3, 4]])

    assert a.__matmul__(2) == NotImplemented

    assert a.__rmatmul__(2) == NotImplemented

    #This is done this way because @ is only supported in Python 3.5+
    #To check 2@a case
    try:
        eval('2 @ a')
    except SyntaxError:
        pass
    except TypeError:  #TypeError is raised in case of NotImplemented is returned
        pass

    #Check a@2 case
    try:
        eval('a @ 2')
    except SyntaxError:
        pass
    except TypeError:  #TypeError is raised in case of NotImplemented is returned
        pass


def test_matmul():
    a = Matrix([[1, 2], [3, 4]])

    assert a.__matmul__(2) == NotImplemented

    assert a.__rmatmul__(2) == NotImplemented

    #This is done this way because @ is only supported in Python 3.5+
    #To check 2@a case
    try:
        eval('2 @ a')
    except SyntaxError:
        pass
    except TypeError:  #TypeError is raised in case of NotImplemented is returned
        pass

    #Check a@2 case
    try:
        eval('a @ 2')
    except SyntaxError:
        pass
    except TypeError:  #TypeError is raised in case of NotImplemented is returned
        pass


def test_matmul(A):
    assert np.all((A @ A.T).todense() == A.dot(A.T).todense())


def test_matmul():
    # https://github.com/pandas-dev/pandas/pull/64267
    df = pd.DataFrame({"a": [1, 2]})

    expr = pd.col("a") @ [3, 4]
    result = df.assign(c=expr)
    expected = pd.DataFrame({"a": [1, 2], "c": [11, 11]})
    tm.assert_frame_equal(result, expected)
    assert str(expr) == "col('a') @ [3, 4]"

    expr = [3, 4] @ pd.col("a")
    result = df.assign(c=expr)
    expected = pd.DataFrame({"a": [1, 2], "c": [11, 11]})
    tm.assert_frame_equal(result, expected)
    assert str(expr) == "[3, 4] @ col('a')"


def test_matmul():
    # np.linalg.matmul and np.matmul only differs in the number
    # of arguments in the signature
    x = np.arange(6).reshape((2, 3))
    actual = np.linalg.matmul(x, x.T)
    expected = np.array([[5, 14], [14, 50]])

    assert_equal(actual, expected)


def test_matmul():
    """
    Test the PEP465 "@" matrix multiplication syntax.
    To avoid syntax errors when importing this file in Python 3.5 and below, we have to use exec() - sorry for that.
    """
    # TODO remove exec() wrapper as soon as we drop support for Python <= 3.5
    if sys.hexversion < 0x30500f0:
        # we are on Python < 3.5
        pytest.skip("'@' (__matmul__) is only supported in Python 3.5 or newer")
    A4 = matrix([[1, 2, 3], [4, 5, 6]])
    A5 = matrix([[6, -1], [3, 2], [0, -3]])
    exec("assert A4 @ A5 == A4 * A5")

