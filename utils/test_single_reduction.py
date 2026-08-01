
def test_single_reduction(name):
    g = Rotation.create_group(name)
    f = g[-1].reduce(g)
    assert_array_almost_equal(f.magnitude(), 0)
    assert f.as_quat().shape == (4,)

