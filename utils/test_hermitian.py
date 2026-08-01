
def test_hermitian():
    H = HermitianOperator('H')

    assert isinstance(H, HermitianOperator)
    assert isinstance(H, Operator)

    assert Dagger(H) == H
    assert H.inv() != H
    assert H.is_commutative is False
    assert Dagger(H).is_commutative is False


def test_hermitian():
    a = Matrix([[1, I], [-I, 1]])
    assert a.is_hermitian
    a[0, 0] = 2*I
    assert a.is_hermitian is False
    a[0, 0] = x
    assert a.is_hermitian is None
    a[0, 1] = a[1, 0]*I
    assert a.is_hermitian is False
    b = HermitianOperator("b")
    c = Operator("c")
    assert Matrix([[b]]).is_hermitian is True
    assert Matrix([[b, c], [Dagger(c), b]]).is_hermitian is True
    assert Matrix([[b, c], [c, b]]).is_hermitian is False
    assert Matrix([[b, c], [transpose(c), b]]).is_hermitian is False


def test_hermitian():
    a = Matrix([[1, I], [-I, 1]])
    assert a.is_hermitian
    a[0, 0] = 2*I
    assert a.is_hermitian is False
    a[0, 0] = x
    assert a.is_hermitian is None
    a[0, 1] = a[1, 0]*I
    assert a.is_hermitian is False


def test_hermitian():
    x = Symbol('x')
    a = SparseMatrix([[0, I], [-I, 0]])
    assert a.is_hermitian
    a = SparseMatrix([[1, I], [-I, 1]])
    assert a.is_hermitian
    a[0, 0] = 2*I
    assert a.is_hermitian is False
    a[0, 0] = x
    assert a.is_hermitian is None
    a[0, 1] = a[1, 0]*I
    assert a.is_hermitian is False


def test_hermitian():
    assert ask(Q.hermitian(x)) is None
    assert ask(Q.hermitian(x), Q.antihermitian(x)) is None
    assert ask(Q.hermitian(x), Q.imaginary(x)) is False
    assert ask(Q.hermitian(x), Q.prime(x)) is True
    assert ask(Q.hermitian(x), Q.real(x)) is True
    assert ask(Q.hermitian(x), Q.zero(x)) is True

    assert ask(Q.hermitian(x + 1), Q.antihermitian(x)) is None
    assert ask(Q.hermitian(x + 1), Q.complex(x)) is None
    assert ask(Q.hermitian(x + 1), Q.hermitian(x)) is True
    assert ask(Q.hermitian(x + 1), Q.imaginary(x)) is False
    assert ask(Q.hermitian(x + 1), Q.real(x)) is True
    assert ask(Q.hermitian(x + I), Q.antihermitian(x)) is None
    assert ask(Q.hermitian(x + I), Q.complex(x)) is None
    assert ask(Q.hermitian(x + I), Q.hermitian(x)) is False
    assert ask(Q.hermitian(x + I), Q.imaginary(x)) is None
    assert ask(Q.hermitian(x + I), Q.real(x)) is False
    assert ask(
        Q.hermitian(x + y), Q.antihermitian(x) & Q.antihermitian(y)) is None
    assert ask(Q.hermitian(x + y), Q.antihermitian(x) & Q.complex(y)) is None
    assert ask(
        Q.hermitian(x + y), Q.antihermitian(x) & Q.hermitian(y)) is None
    assert ask(Q.hermitian(x + y), Q.antihermitian(x) & Q.imaginary(y)) is None
    assert ask(Q.hermitian(x + y), Q.antihermitian(x) & Q.real(y)) is None
    assert ask(Q.hermitian(x + y), Q.hermitian(x) & Q.complex(y)) is None
    assert ask(Q.hermitian(x + y), Q.hermitian(x) & Q.hermitian(y)) is True
    assert ask(Q.hermitian(x + y), Q.hermitian(x) & Q.imaginary(y)) is False
    assert ask(Q.hermitian(x + y), Q.hermitian(x) & Q.real(y)) is True
    assert ask(Q.hermitian(x + y), Q.imaginary(x) & Q.complex(y)) is None
    assert ask(Q.hermitian(x + y), Q.imaginary(x) & Q.imaginary(y)) is None
    assert ask(Q.hermitian(x + y), Q.imaginary(x) & Q.real(y)) is False
    assert ask(Q.hermitian(x + y), Q.real(x) & Q.complex(y)) is None
    assert ask(Q.hermitian(x + y), Q.real(x) & Q.real(y)) is True

    assert ask(Q.hermitian(I*x), Q.antihermitian(x)) is True
    assert ask(Q.hermitian(I*x), Q.complex(x)) is None
    assert ask(Q.hermitian(I*x), Q.hermitian(x)) is False
    assert ask(Q.hermitian(I*x), Q.imaginary(x)) is True
    assert ask(Q.hermitian(I*x), Q.real(x)) is False
    assert ask(Q.hermitian(x*y), Q.hermitian(x) & Q.real(y)) is True

    assert ask(
        Q.hermitian(x + y + z), Q.real(x) & Q.real(y) & Q.real(z)) is True
    assert ask(Q.hermitian(x + y + z),
        Q.real(x) & Q.real(y) & Q.imaginary(z)) is False
    assert ask(Q.hermitian(x + y + z),
        Q.real(x) & Q.imaginary(y) & Q.imaginary(z)) is None
    assert ask(Q.hermitian(x + y + z),
        Q.imaginary(x) & Q.imaginary(y) & Q.imaginary(z)) is None

    assert ask(Q.antihermitian(x)) is None
    assert ask(Q.antihermitian(x), Q.real(x)) is False
    assert ask(Q.antihermitian(x), Q.prime(x)) is False

    assert ask(Q.antihermitian(x + 1), Q.antihermitian(x)) is False
    assert ask(Q.antihermitian(x + 1), Q.complex(x)) is None
    assert ask(Q.antihermitian(x + 1), Q.hermitian(x)) is None
    assert ask(Q.antihermitian(x + 1), Q.imaginary(x)) is False
    assert ask(Q.antihermitian(x + 1), Q.real(x)) is None
    assert ask(Q.antihermitian(x + I), Q.antihermitian(x)) is True
    assert ask(Q.antihermitian(x + I), Q.complex(x)) is None
    assert ask(Q.antihermitian(x + I), Q.hermitian(x)) is None
    assert ask(Q.antihermitian(x + I), Q.imaginary(x)) is True
    assert ask(Q.antihermitian(x + I), Q.real(x)) is False
    assert ask(Q.antihermitian(x), Q.zero(x)) is True

    assert ask(
        Q.antihermitian(x + y), Q.antihermitian(x) & Q.antihermitian(y)
    ) is True
    assert ask(
        Q.antihermitian(x + y), Q.antihermitian(x) & Q.complex(y)) is None
    assert ask(
        Q.antihermitian(x + y), Q.antihermitian(x) & Q.hermitian(y)) is None
    assert ask(
        Q.antihermitian(x + y), Q.antihermitian(x) & Q.imaginary(y)) is True
    assert ask(Q.antihermitian(x + y), Q.antihermitian(x) & Q.real(y)
        ) is False
    assert ask(Q.antihermitian(x + y), Q.hermitian(x) & Q.complex(y)) is None
    assert ask(Q.antihermitian(x + y), Q.hermitian(x) & Q.hermitian(y)
        ) is None
    assert ask(
        Q.antihermitian(x + y), Q.hermitian(x) & Q.imaginary(y)) is None
    assert ask(Q.antihermitian(x + y), Q.hermitian(x) & Q.real(y)) is None
    assert ask(Q.antihermitian(x + y), Q.imaginary(x) & Q.complex(y)) is None
    assert ask(Q.antihermitian(x + y), Q.imaginary(x) & Q.imaginary(y)) is True
    assert ask(Q.antihermitian(x + y), Q.imaginary(x) & Q.real(y)) is False
    assert ask(Q.antihermitian(x + y), Q.real(x) & Q.complex(y)) is None
    assert ask(Q.antihermitian(x + y), Q.real(x) & Q.real(y)) is None

    assert ask(Q.antihermitian(I*x), Q.real(x)) is True
    assert ask(Q.antihermitian(I*x), Q.antihermitian(x)) is False
    assert ask(Q.antihermitian(I*x), Q.complex(x)) is None
    assert ask(Q.antihermitian(x*y), Q.antihermitian(x) & Q.real(y)) is True

    assert ask(Q.antihermitian(x + y + z),
        Q.real(x) & Q.real(y) & Q.real(z)) is None
    assert ask(Q.antihermitian(x + y + z),
        Q.real(x) & Q.real(y) & Q.imaginary(z)) is None
    assert ask(Q.antihermitian(x + y + z),
        Q.real(x) & Q.imaginary(y) & Q.imaginary(z)) is False
    assert ask(Q.antihermitian(x + y + z),
        Q.imaginary(x) & Q.imaginary(y) & Q.imaginary(z)) is True


def test_hermitian():
    """Check complex-value Hermitian cases.
    """
    rnd = np.random.RandomState(0)

    sizes = [3, 12]
    ks = [1, 2]
    gens = [True, False]

    for s, k, gen, dh, dx, db in (
        itertools.product(sizes, ks, gens, gens, gens, gens)
    ):
        H = rnd.random((s, s)) + 1.j * rnd.random((s, s))
        H = 10 * np.eye(s) + H + H.T.conj()
        H = H.astype(np.complex128) if dh else H.astype(np.complex64)

        X = rnd.standard_normal((s, k))
        X = X + 1.j * rnd.standard_normal((s, k))
        X = X.astype(np.complex128) if dx else X.astype(np.complex64)

        if not gen:
            B = np.eye(s)
            w, v = lobpcg(H, X, maxiter=99, verbosityLevel=0)
            # Also test mixing complex H with real B.
            wb, _ = lobpcg(H, X, B, maxiter=99, verbosityLevel=0)
            assert_allclose(w, wb, rtol=1e-6)
            w0, _ = eigh(H)
        else:
            B = rnd.random((s, s)) + 1.j * rnd.random((s, s))
            B = 10 * np.eye(s) + B.dot(B.T.conj())
            B = B.astype(np.complex128) if db else B.astype(np.complex64)
            w, v = lobpcg(H, X, B, maxiter=99, verbosityLevel=0)
            w0, _ = eigh(H, B)

        for wx, vx in zip(w, v.T):
            # Check eigenvector
            assert_allclose(np.linalg.norm(H.dot(vx) - B.dot(vx) * wx)
                            / np.linalg.norm(H.dot(vx)),
                            0, atol=5e-2, rtol=0)

            # Compare eigenvalues
            j = np.argmin(abs(w0 - wx))
            assert_allclose(wx, w0[j], rtol=1e-4)

