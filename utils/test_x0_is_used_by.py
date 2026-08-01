
def test_x0_is_used_by(problem_func):
    A, b = problem_func()
    # Random x0 to feed minres
    rng = np.random.RandomState(12345)
    x0 = rng.rand(10)
    trace = []

    def trace_iterates(xk):
        trace.append(xk)
    minres(A, b, x0=x0, callback=trace_iterates)
    trace_with_x0 = trace

    trace = []
    minres(A, b, callback=trace_iterates)
    assert_(not np.array_equal(trace_with_x0[0], trace[0]))

