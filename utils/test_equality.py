
def test_equality():
    first_list = [1, 2, 3, 4]
    second_list = [1, 2, 3, 4]
    third_list = [4, 3, 2, 1]
    assert first_list == second_list
    assert first_list != third_list

    first_ndim_array = ImmutableDenseNDimArray(first_list, (2, 2))
    second_ndim_array = ImmutableDenseNDimArray(second_list, (2, 2))
    fourth_ndim_array = ImmutableDenseNDimArray(first_list, (2, 2))

    assert first_ndim_array == second_ndim_array

    def assignment_attempt(a):
        a[0, 0] = 0

    raises(TypeError, lambda: assignment_attempt(second_ndim_array))
    assert first_ndim_array == second_ndim_array
    assert first_ndim_array == fourth_ndim_array


def test_equality():
    first_list = [1, 2, 3, 4]
    second_list = [1, 2, 3, 4]
    third_list = [4, 3, 2, 1]
    assert first_list == second_list
    assert first_list != third_list

    first_ndim_array = MutableDenseNDimArray(first_list, (2, 2))
    second_ndim_array = MutableDenseNDimArray(second_list, (2, 2))
    third_ndim_array = MutableDenseNDimArray(third_list, (2, 2))
    fourth_ndim_array = MutableDenseNDimArray(first_list, (2, 2))

    assert first_ndim_array == second_ndim_array
    second_ndim_array[0, 0] = 0
    assert first_ndim_array != second_ndim_array
    assert first_ndim_array != third_ndim_array
    assert first_ndim_array == fourth_ndim_array


def test_equality():
    a, b, c = Identity(3), eye(3), ImmutableMatrix(eye(3))
    for x in [a, b, c]:
        for y in [a, b, c]:
            assert x.equals(y)


def test_equality():
    A = Matrix(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
    B = Matrix(((9, 8, 7), (6, 5, 4), (3, 2, 1)))
    assert A == A[:, :]
    assert not A != A[:, :]
    assert not A == B
    assert A != B
    assert A != 10
    assert not A == 10

    # A SparseMatrix can be equal to a Matrix
    C = SparseMatrix(((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    D = Matrix(((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    assert C == D
    assert not C != D


def test_equality():
    A = Matrix(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
    B = Matrix(((9, 8, 7), (6, 5, 4), (3, 2, 1)))
    assert A == A[:, :]
    assert not A != A[:, :]
    assert not A == B
    assert A != B
    assert A != 10
    assert not A == 10

    # A SparseMatrix can be equal to a Matrix
    C = SparseMatrix(((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    D = Matrix(((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    assert C == D
    assert not C != D


def test_equality():
    instances = [b1, b2, b3, b21, Basic(b1, b1, b1), Basic]
    for i, b_i in enumerate(instances):
        for j, b_j in enumerate(instances):
            assert (b_i == b_j) == (i == j)
            assert (b_i != b_j) == (i != j)

    assert Basic() != []
    assert not(Basic() == [])
    assert Basic() != 0
    assert not(Basic() == 0)

    class Foo:
        """
        Class that is unaware of Basic, and relies on both classes returning
        the NotImplemented singleton for equivalence to evaluate to False.

        """

    b = Basic()
    foo = Foo()

    assert b != foo
    assert foo != b
    assert not b == foo
    assert not foo == b

    class Bar:
        """
        Class that considers itself equal to any instance of Basic, and relies
        on Basic returning the NotImplemented singleton in order to achieve
        a symmetric equivalence relation.

        """
        def __eq__(self, other):
            if isinstance(other, Basic):
                return True
            return NotImplemented

        def __ne__(self, other):
            return not self == other

    bar = Bar()

    assert b == bar
    assert bar == b
    assert not b != bar
    assert not bar != b


def test_equality():
    # if this fails remove special handling below
    raises(ValueError, lambda: Sum(x, x))
    r = symbols('x', real=True)
    for F in (Sum, Product, Integral):
        try:
            assert F(x, x) != F(y, y)
            assert F(x, (x, 1, 2)) != F(x, x)
            assert F(x, (x, x)) != F(x, x)  # or else they print the same
            assert F(1, x) != F(1, y)
        except ValueError:
            pass
        assert F(a, (x, 1, 2)) != F(a, (x, 1, 3))  # diff limit
        assert F(a, (x, 1, x)) != F(a, (y, 1, y))
        assert F(a, (x, 1, 2)) != F(b, (x, 1, 2))  # diff expression
        assert F(x, (x, 1, 2)) != F(r, (r, 1, 2))  # diff assumptions
        assert F(1, (x, 1, x)) != F(1, (y, 1, x))  # only dummy is diff
        assert F(1, (x, 1, x)).dummy_eq(F(1, (y, 1, x)))

    # issue 5265
    assert Sum(x, (x, 1, x)).subs(x, a) == Sum(x, (x, 1, a))


def test_equality():
    p_1 = Permutation(0, 1, 3)
    p_2 = Permutation(0, 2, 3)
    p_3 = Permutation(0, 1, 2)
    p_4 = Permutation(0, 1, 3)
    g_1 = PermutationGroup(p_1, p_2)
    g_2 = PermutationGroup(p_3, p_4)
    g_3 = PermutationGroup(p_2, p_1)
    g_4 = PermutationGroup(p_1, p_2)

    assert g_1 != g_2
    assert g_1.generators != g_2.generators
    assert g_1.equals(g_2)
    assert g_1 != g_3
    assert g_1.equals(g_3)
    assert g_1 == g_4


def test_equality():
    # test symmetry and reflexivity
    assert ask(Q.eq(x, x)) is True
    assert ask(Q.eq(y, x), Q.eq(x, y)) is True
    assert ask(Q.eq(y, x), ~Q.eq(z, z) | Q.eq(x, y)) is True

    # test transitivity
    assert ask(Q.eq(x,z), Q.eq(x,y) & Q.eq(y,z)) is True

