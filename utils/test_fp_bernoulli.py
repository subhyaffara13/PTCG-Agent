
def test_fp_bernoulli():
    assert ae(fp.bernoulli(0), 1.0)
    assert ae(fp.bernoulli(1), -0.5)
    assert ae(fp.bernoulli(2), 0.16666666666666666667)
    assert ae(fp.bernoulli(10), 0.075757575757575757576)
    assert ae(fp.bernoulli(11), 0.0)

