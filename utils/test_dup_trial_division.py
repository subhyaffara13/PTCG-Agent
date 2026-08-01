
def test_dup_trial_division():
    R, x = ring("x", ZZ)
    assert R.dup_trial_division(x**5 + 8*x**4 + 25*x**3 + 38*x**2 + 28*x + 8, (x + 1, x + 2)) == [(x + 1, 2), (x + 2, 3)]

