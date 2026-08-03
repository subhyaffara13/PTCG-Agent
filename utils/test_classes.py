import sys

def test_classes():
    y0 = [1 / 3, 2 / 9]
    for cls in [RK23, RK45, DOP853, Radau, BDF, LSODA]:
        solver = cls(fun_rational, 5, y0, np.inf)
        assert_equal(solver.n, 2)
        assert_equal(solver.status, 'running')
        assert_equal(solver.t_bound, np.inf)
        assert_equal(solver.direction, 1)
        assert_equal(solver.t, 5)
        assert_equal(solver.y, y0)
        assert_(solver.step_size is None)
        if cls is not LSODA:
            assert_(solver.nfev > 0)
            assert_(solver.njev >= 0)
            assert_equal(solver.nlu, 0)
        else:
            assert_equal(solver.nfev, 0)
            assert_equal(solver.njev, 0)
            assert_equal(solver.nlu, 0)

        assert_raises(RuntimeError, solver.dense_output)

        message = solver.step()
        assert_equal(solver.status, 'running')
        assert_equal(message, None)
        assert_equal(solver.n, 2)
        assert_equal(solver.t_bound, np.inf)
        assert_equal(solver.direction, 1)
        assert_(solver.t > 5)
        assert_(not np.all(np.equal(solver.y, y0)))
        assert_(solver.step_size > 0)
        assert_(solver.nfev > 0)
        assert_(solver.njev >= 0)
        assert_(solver.nlu >= 0)
        sol = solver.dense_output()
        assert_allclose(sol(5), y0, rtol=1e-15, atol=0)


def test_classes():
  from io import BytesIO as StringIO
  y = "from _io import BytesIO\n"
  x = y if (IS_PYPY or sys.hexversion >= PY310b) else "from io import BytesIO\n"
  s = StringIO()

  assert getimport(StringIO) == x
  assert getimport(s) == y
  # interactively defined classes and class instances
  assert getimport(Foo) == 'from %s import Foo\n' % __name__
  assert getimport(_foo) == 'from %s import Foo\n' % __name__

