
def test_args():
    for n, cls in enumerate(classes):
        m = cls.zeros(3, 2)
        # all should give back the same type of arguments, e.g. ints for shape
        assert m.shape == (3, 2) and all(type(i) is int for i in m.shape)
        assert m.rows == 3 and type(m.rows) is int
        assert m.cols == 2 and type(m.cols) is int
        if not n % 2:
            assert type(m.flat()) in (list, tuple, Tuple)
        else:
            assert type(m.todok()) is dict


def test_args():
    for n, cls in enumerate(all_classes):
        m = cls.zeros(3, 2)
        # all should give back the same type of arguments, e.g. ints for shape
        assert m.shape == (3, 2) and all(type(i) is int for i in m.shape)
        assert m.rows == 3 and type(m.rows) is int
        assert m.cols == 2 and type(m.cols) is int
        if not n % 2:
            assert type(m.flat()) in (list, tuple, Tuple)
        else:
            assert type(m.todok()) is dict


def test_args():
    assert (x*y).args in ((x, y), (y, x))
    assert (x + y).args in ((x, y), (y, x))
    assert (x*y + 1).args in ((x*y, 1), (1, x*y))
    assert sin(x*y).args == (x*y,)
    assert sin(x*y).args[0] == x*y
    assert (x**y).args == (x, y)
    assert (x**y).args[0] == x
    assert (x**y).args[1] == y


def test_args():
    p = Permutation([(0, 3, 1, 2), (4, 5)])
    assert p._cyclic_form is None
    assert Permutation(p) == p
    assert p.cyclic_form == [[0, 3, 1, 2], [4, 5]]
    assert p._array_form == [3, 2, 0, 1, 5, 4]
    p = Permutation((0, 3, 1, 2))
    assert p._cyclic_form is None
    assert p._array_form == [0, 3, 1, 2]
    assert Permutation([0]) == Permutation((0, ))
    assert Permutation([[0], [1]]) == Permutation(((0, ), (1, ))) == \
        Permutation(((0, ), [1]))
    assert Permutation([[1, 2]]) == Permutation([0, 2, 1])
    assert Permutation([[1], [4, 2]]) == Permutation([0, 1, 4, 3, 2])
    assert Permutation([[1], [4, 2]], size=1) == Permutation([0, 1, 4, 3, 2])
    assert Permutation(
        [[1], [4, 2]], size=6) == Permutation([0, 1, 4, 3, 2, 5])
    assert Permutation([[0, 1], [0, 2]]) == Permutation(0, 1, 2)
    assert Permutation([], size=3) == Permutation([0, 1, 2])
    assert Permutation(3).list(5) == [0, 1, 2, 3, 4]
    assert Permutation(3).list(-1) == []
    assert Permutation(5)(1, 2).list(-1) == [0, 2, 1]
    assert Permutation(5)(1, 2).list() == [0, 2, 1, 3, 4, 5]
    raises(ValueError, lambda: Permutation([1, 2], [0]))
           # enclosing brackets needed
    raises(ValueError, lambda: Permutation([[1, 2], 0]))
           # enclosing brackets needed on 0
    raises(ValueError, lambda: Permutation([1, 1, 0]))
    raises(ValueError, lambda: Permutation([4, 5], size=10))  # where are 0-3?
    # but this is ok because cycles imply that only those listed moved
    assert Permutation(4, 5) == Permutation([0, 1, 2, 3, 5, 4])


def test_args():
    A = eye(3)
    # Nonsquare array
    with pytest.raises(ValueError):
        ldl(A[:, :2])
    # Complex matrix with imaginary diagonal entries with "hermitian=True"
    with pytest.warns(ComplexWarning):
        ldl(A*1j)


def test_args():

    # sys3 is actually two decoupled systems. (x, y) form a
    # linear oscillator, while z is a nonlinear first order
    # system with equilibria at z=0 and z=1. If k > 0, z=1
    # is stable and z=0 is unstable.

    def sys3(t, w, omega, k, zfinal):
        x, y, z = w
        return [-omega*y, omega*x, k*z*(1 - z)]

    def sys3_jac(t, w, omega, k, zfinal):
        x, y, z = w
        J = np.array([[0, -omega, 0],
                      [omega, 0, 0],
                      [0, 0, k*(1 - 2*z)]])
        return J

    def sys3_x0decreasing(t, w, omega, k, zfinal):
        x, y, z = w
        return x

    def sys3_y0increasing(t, w, omega, k, zfinal):
        x, y, z = w
        return y

    def sys3_zfinal(t, w, omega, k, zfinal):
        x, y, z = w
        return z - zfinal

    # Set the event flags for the event functions.
    sys3_x0decreasing.direction = -1
    sys3_y0increasing.direction = 1
    sys3_zfinal.terminal = True

    omega = 2
    k = 4

    tfinal = 5
    zfinal = 0.99
    # Find z0 such that when z(0) = z0, z(tfinal) = zfinal.
    # The condition z(tfinal) = zfinal is the terminal event.
    z0 = np.exp(-k*tfinal)/((1 - zfinal)/zfinal + np.exp(-k*tfinal))

    w0 = [0, -1, z0]

    # Provide the jac argument and use the Radau method to ensure that the use
    # of the Jacobian function is exercised.
    # If event handling is working, the solution will stop at tfinal, not tend.
    tend = 2*tfinal
    sol = solve_ivp(sys3, [0, tend], w0,
                    events=[sys3_x0decreasing, sys3_y0increasing, sys3_zfinal],
                    dense_output=True, args=(omega, k, zfinal),
                    method='Radau', jac=sys3_jac,
                    rtol=1e-10, atol=1e-13)

    # Check that we got the expected events at the expected times.
    x0events_t = sol.t_events[0]
    y0events_t = sol.t_events[1]
    zfinalevents_t = sol.t_events[2]
    assert_allclose(x0events_t, [0.5*np.pi, 1.5*np.pi])
    assert_allclose(y0events_t, [0.25*np.pi, 1.25*np.pi])
    assert_allclose(zfinalevents_t, [tfinal])

    # Check that the solution agrees with the known exact solution.
    t = np.linspace(0, zfinalevents_t[0], 250)
    w = sol.sol(t)
    assert_allclose(w[0], np.sin(omega*t), rtol=1e-9, atol=1e-12)
    assert_allclose(w[1], -np.cos(omega*t), rtol=1e-9, atol=1e-12)
    assert_allclose(w[2], 1/(((1 - z0)/z0)*np.exp(-k*t) + 1),
                    rtol=1e-9, atol=1e-12)

    # Check that the state variables have the expected values at the events.
    x0events = sol.sol(x0events_t)
    y0events = sol.sol(y0events_t)
    zfinalevents = sol.sol(zfinalevents_t)
    assert_allclose(x0events[0], np.zeros_like(x0events[0]), atol=5e-14)
    assert_allclose(x0events[1], np.ones_like(x0events[1]))
    assert_allclose(y0events[0], np.ones_like(y0events[0]))
    assert_allclose(y0events[1], np.zeros_like(y0events[1]), atol=5e-14)
    assert_allclose(zfinalevents[2], [zfinal])

