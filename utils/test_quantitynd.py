
def test_quantitynd():
    q = QuantityND([1, 2], "m")
    q0, q1 = q[:]
    assert np.all(q.v == np.asarray([1, 2]))
    assert q.units == "m"
    assert np.all((q0 + q1).v == np.asarray([3]))
    assert (q0 * q1).units == "m*m"
    assert (q1 / q0).units == "m/(m)"
    with pytest.raises(ValueError):
        q0 + QuantityND(1, "s")

