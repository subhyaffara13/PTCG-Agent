
def test_ufunc_with_output():
    # check that giving an output argument always returns that output.
    # Regression test for gh-8416.
    x = array([1., 2., 3.], mask=[0, 0, 1])
    y = np.add(x, 1., out=x)
    assert_(y is x)

