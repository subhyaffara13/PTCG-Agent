
def test_maxiter_int_check_gh10236(method):
    # gh-10236 reported that the error message when `maxiter` is not an integer
    # was difficult to interpret. Check that this was resolved (by gh-10907).
    message = "'float' object cannot be interpreted as an integer"
    with pytest.raises(TypeError, match=message):
        method(f1, 0.0, 1.0, maxiter=72.45)

