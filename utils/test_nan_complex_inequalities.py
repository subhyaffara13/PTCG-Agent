
def test_nan_complex_inequalities():
    # Comparisons of NaN with non-real raise errors, we're not too
    # fussy whether its the NaN error or complex error.
    for r in (I, zoo, Symbol('z', imaginary=True)):
        assert_all_ineq_raise_TypeError(r, nan)

