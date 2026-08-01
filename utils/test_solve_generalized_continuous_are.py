
def test_solve_generalized_continuous_are():
    cases = [
        # Two random examples differ by s term
        # in the absence of any literature for demanding examples.
        (np.array([[2.769230e-01, 8.234578e-01, 9.502220e-01],
                   [4.617139e-02, 6.948286e-01, 3.444608e-02],
                   [9.713178e-02, 3.170995e-01, 4.387444e-01]]),
         np.array([[3.815585e-01, 1.868726e-01],
                   [7.655168e-01, 4.897644e-01],
                   [7.951999e-01, 4.455862e-01]]),
         np.eye(3),
         np.eye(2),
         np.array([[6.463130e-01, 2.760251e-01, 1.626117e-01],
                   [7.093648e-01, 6.797027e-01, 1.189977e-01],
                   [7.546867e-01, 6.550980e-01, 4.983641e-01]]),
         np.zeros((3, 2)),
         None),
        (np.array([[2.769230e-01, 8.234578e-01, 9.502220e-01],
                   [4.617139e-02, 6.948286e-01, 3.444608e-02],
                   [9.713178e-02, 3.170995e-01, 4.387444e-01]]),
         np.array([[3.815585e-01, 1.868726e-01],
                   [7.655168e-01, 4.897644e-01],
                   [7.951999e-01, 4.455862e-01]]),
         np.eye(3),
         np.eye(2),
         np.array([[6.463130e-01, 2.760251e-01, 1.626117e-01],
                   [7.093648e-01, 6.797027e-01, 1.189977e-01],
                   [7.546867e-01, 6.550980e-01, 4.983641e-01]]),
         np.ones((3, 2)),
         None)
        ]

    min_decimal = (10, 10)

    def _test_factory(case, dec):
        """Checks if X = A'XA-(A'XB)(R+B'XB)^-1(B'XA)+Q) is true"""
        a, b, q, r, e, s, knownfailure = case
        if knownfailure:
            pytest.xfail(reason=knownfailure)

        x = solve_continuous_are(a, b, q, r, e, s)
        res = a.conj().T.dot(x.dot(e)) + e.conj().T.dot(x.dot(a)) + q
        out_fact = e.conj().T.dot(x).dot(b) + s
        res -= out_fact.dot(solve(np.atleast_2d(r), out_fact.conj().T))
        assert_array_almost_equal(res, np.zeros_like(res), decimal=dec)

    for ind, case in enumerate(cases):
        _test_factory(case, min_decimal[ind])

