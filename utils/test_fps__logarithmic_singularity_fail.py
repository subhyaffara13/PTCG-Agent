
def test_fps__logarithmic_singularity_fail():
    f = asech(x)  # Algorithms for computing limits probably needs improvements
    assert fps(f, x) == log(2) - log(x) - x**2/4 - 3*x**4/64 + O(x**6)

