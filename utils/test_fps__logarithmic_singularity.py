
def test_fps__logarithmic_singularity():
    f = log(1 + 1/x)
    assert fps(f, x) != \
        -log(x) + x - x**2/2 + x**3/3 - x**4/4 + x**5/5 + O(x**6)
    assert fps(f, x, rational=False) != \
        -log(x) + x - x**2/2 + x**3/3 - x**4/4 + x**5/5 + O(x**6)

