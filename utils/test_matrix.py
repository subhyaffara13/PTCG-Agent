
def test_matrix():
    A = Matrix([[x, x*y], [sin(z) + 4, x**z]])
    sol = Matrix([[1, 2], [sin(3) + 4, 1]])
    f = lambdify((x, y, z), A, modules="sympy")
    assert f(1, 2, 3) == sol
    f = lambdify((x, y, z), (A, [A]), modules="sympy")
    assert f(1, 2, 3) == (sol, [sol])
    J = Matrix((x, x + y)).jacobian((x, y))
    v = Matrix((x, y))
    sol = Matrix([[1, 0], [1, 1]])
    assert lambdify(v, J, modules='sympy')(1, 2) == sol
    assert lambdify(v.T, J, modules='sympy')(1, 2) == sol


def test_matrix():
    from sympy.matrices.expressions.matexpr import MatrixSymbol
    X = MatrixSymbol('X', n, n)
    Y = MatrixSymbol('Y', 2, 2)
    Z = MatrixSymbol('Z', 2, 3)
    assert list(unify(X, Y, {}, variables=[n, Str('X')])) == [{Str('X'): Str('Y'), n: 2}]
    assert list(unify(X, Z, {}, variables=[n, Str('X')])) == []


def test_matrix():
    # Test printing a Matrix that has an element that is printed differently
    # with the LambdaPrinter than with the StrPrinter.
    e = x % 2
    assert lambdarepr(e) != str(e)
    assert lambdarepr(Matrix([e])) == 'ImmutableDenseMatrix([[x % 2]])'


def test_matrix():
    assert rust_code(Matrix([1, 2, 3])) == '[1, 2, 3]'
    with raises(ValueError):
        rust_code(Matrix([[1, 2, 3]]))


def test_matrix():
    x = symbols('x')
    m = Matrix([[I, x*I], [2, 4]])
    assert Dagger(m) == m.H


def test_matrix():

    # hermitian
    assert ask(Q.hermitian(Matrix([[2, 2 + I, 4], [2 - I, 3, I], [4, -I, 1]]))) == True
    assert ask(Q.hermitian(Matrix([[2, 2 + I, 4], [2 + I, 3, I], [4, -I, 1]]))) == False
    z = symbols('z', complex=True)
    assert ask(Q.hermitian(Matrix([[2, 2 + I, z], [2 - I, 3, I], [4, -I, 1]]))) == None
    assert ask(Q.hermitian(SparseMatrix(((25, 15, -5), (15, 18, 0), (-5, 0, 11))))) == True
    assert ask(Q.hermitian(SparseMatrix(((25, 15, -5), (15, I, 0), (-5, 0, 11))))) == False
    assert ask(Q.hermitian(SparseMatrix(((25, 15, -5), (15, z, 0), (-5, 0, 11))))) == None

    # antihermitian
    A = Matrix([[0, -2 - I, 0], [2 - I, 0, -I], [0, -I, 0]])
    B = Matrix([[-I, 2 + I, 0], [-2 + I, 0, 2 + I], [0, -2 + I, -I]])
    assert ask(Q.antihermitian(A)) is True
    assert ask(Q.antihermitian(B)) is True
    assert ask(Q.antihermitian(A**2)) is False
    C = (B**3)
    C.simplify()
    assert ask(Q.antihermitian(C)) is True
    _A = Matrix([[0, -2 - I, 0], [z, 0, -I], [0, -I, 0]])
    assert ask(Q.antihermitian(_A)) is None

