
def test_matrix_exponential_issue_26821():
    # The symbol names matter in the original bug...
    a, b, c, d, e = symbols("Tau, Tau_syn_in, Tau_syn_ex, C_m, Tau_syn_gap")
    t = symbols("__h")
    M = Matrix([
        [      0,  1.0,       0,    0,       0,    0,    0],
        [-1/b**2, -2/b,       0,    0,       0,    0,    0],
        [      0,    0,       0,  1.0,       0,    0,    0],
        [      0,    0, -1/c**2, -2/c,       0,    0,    0],
        [      0,    0,       0,    0,       0,    1,    0],
        [      0,    0,       0,    0, -1/e**2, -2/e,    0],
        [    1/d,    0,     1/d,    0,     1/d,    0, -1/a]
    ])

    Me = (t*M).exp()
    assert (Me.diff(t) - M*Me).applyfunc(cancel) == zeros(7)
    # https://github.com/sympy/sympy/issues/26821
    # Previously very large floats were in the result.
    assert max(abs(f) for f in Me.atoms(Float)) < 1e3

