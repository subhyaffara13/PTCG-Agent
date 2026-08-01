
def test_comapre_not_instance():
    w = OmegaPower(omega + 1, 1)
    assert(not (w == None))
    assert(not (w < 5))
    raises(TypeError, lambda: w < 6.66)

