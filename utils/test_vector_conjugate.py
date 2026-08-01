
def test_vector_conjugate():
    # https://github.com/sympy/sympy/issues/27094
    assert (I*i + (1 + I)*j + 2*k).conjugate() == -I*i + (1 - I)*j + 2*k

