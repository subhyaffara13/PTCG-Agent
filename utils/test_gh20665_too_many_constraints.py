
def test_gh20665_too_many_constraints():
    # gh-20665 reports a confusing error message when there are more equality
    # constraints than variables. Check that the error message is improved.
    message = "...more equality constraints than independent variables..."
    with pytest.raises(ValueError, match=message):
        x0 = np.ones((2,))
        A_eq, b_eq = np.arange(6).reshape((3, 2)), np.ones((3,))
        g = NonlinearConstraint(lambda x:  A_eq @ x, lb=b_eq, ub=b_eq)
        minimize(rosen, x0, method='trust-constr', constraints=[g])
    # no error with `SVDFactorization`
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        minimize(rosen, x0, method='trust-constr', constraints=[g],
                 options={'factorization_method': 'SVDFactorization'})

