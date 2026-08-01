
def test_dft():
    n, i, j = symbols('n i j')
    assert DFT(4).shape == (4, 4)
    assert ask(Q.unitary(DFT(4)))
    assert Abs(simplify(det(Matrix(DFT(4))))) == 1
    assert DFT(n)*IDFT(n) == Identity(n)
    assert DFT(n)[i, j] == exp(-2*S.Pi*I/n)**(i*j) / sqrt(n)


def test_dft():
    m = dft(2)
    expected = array([[1.0, 1.0], [1.0, -1.0]])
    assert_array_almost_equal(m, expected)
    m = dft(2, scale='n')
    assert_array_almost_equal(m, expected/2.0)
    m = dft(2, scale='sqrtn')
    assert_array_almost_equal(m, expected/sqrt(2.0))

    x = array([0, 1, 2, 3, 4, 5, 0, 1])
    m = dft(8)
    mx = m.dot(x)
    fx = fft(x)
    assert_array_almost_equal(mx, fx)

