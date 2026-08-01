
def test_evalf_oo_to_oo():
    # There used to be an error in certain cases
    # Does not evaluate, but at least do not throw an error
    # Evaluates symbolically to 0, which is not correct
    assert Sum(1/(n**2+1), (n, -oo, oo)).evalf() == Sum(1/(n**2+1), (n, -oo, oo))
    # This evaluates if from 1 to oo and symbolically
    assert Sum(1/(factorial(abs(n))), (n, -oo, -1)).evalf() == Sum(1/(factorial(abs(n))), (n, -oo, -1))

