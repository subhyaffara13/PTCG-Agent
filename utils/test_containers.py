
def test_containers():
    assert julia_code([1, 2, 3, [4, 5, [6, 7]], 8, [9, 10], 11]) == \
        "Any[1, 2, 3, Any[4, 5, Any[6, 7]], 8, Any[9, 10], 11]"
    assert julia_code((1, 2, (3, 4))) == "(1, 2, (3, 4))"
    assert julia_code([1]) == "Any[1]"
    assert julia_code((1,)) == "(1,)"
    assert julia_code(Tuple(*[1, 2, 3])) == "(1, 2, 3)"
    assert julia_code((1, x*y, (3, x**2))) == "(1, x .* y, (3, x .^ 2))"
    # scalar, matrix, empty matrix and empty list
    assert julia_code((1, eye(3), Matrix(0, 0, []), [])) == "(1, [1 0 0;\n0 1 0;\n0 0 1], zeros(0, 0), Any[])"


def test_containers():
    assert maple_code([1, 2, 3, [4, 5, [6, 7]], 8, [9, 10], 11]) == \
           "[1, 2, 3, [4, 5, [6, 7]], 8, [9, 10], 11]"

    assert maple_code((1, 2, (3, 4))) == "[1, 2, [3, 4]]"
    assert maple_code([1]) == "[1]"
    assert maple_code((1,)) == "[1]"
    assert maple_code(Tuple(*[1, 2, 3])) == "[1, 2, 3]"
    assert maple_code((1, x * y, (3, x ** 2))) == "[1, x*y, [3, x^2]]"
    # scalar, matrix, empty matrix and empty list

    assert maple_code((1, eye(3), Matrix(0, 0, []), [])) == \
           "[1, Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]], storage = rectangular), Matrix([], storage = rectangular), []]"


def test_containers():
    assert mcode([1, 2, 3, [4, 5, [6, 7]], 8, [9, 10], 11]) == \
        "{1, 2, 3, {4, 5, {6, 7}}, 8, {9, 10}, 11}"
    assert mcode((1, 2, (3, 4))) == "{1, 2, {3, 4}}"
    assert mcode([1]) == "{1}"
    assert mcode((1,)) == "{1}"
    assert mcode(Tuple(*[1, 2, 3])) == "{1, 2, 3}"


def test_containers():
    assert mcode([1, 2, 3, [4, 5, [6, 7]], 8, [9, 10], 11]) == \
        "{1, 2, 3, {4, 5, {6, 7}}, 8, {9, 10}, 11}"
    assert mcode((1, 2, (3, 4))) == "{1, 2, {3, 4}}"
    assert mcode([1]) == "{1}"
    assert mcode((1,)) == "{1}"
    assert mcode(Tuple(*[1, 2, 3])) == "{1, 2, 3}"
    assert mcode((1, x*y, (3, x**2))) == "{1, x.*y, {3, x.^2}}"
    # scalar, matrix, empty matrix and empty list
    assert mcode((1, eye(3), Matrix(0, 0, []), [])) == "{1, [1 0 0; 0 1 0; 0 0 1], [], {}}"

