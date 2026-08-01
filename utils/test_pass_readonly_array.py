
def test_pass_readonly_array():
    z = np.full((5, 6), 42.0)
    z.flags.writeable = False
    np.testing.assert_array_equal(z, m.fixed_copy_r(z))
    np.testing.assert_array_equal(m.fixed_r_const(), m.fixed_r())
    assert not m.fixed_r_const().flags.writeable
    np.testing.assert_array_equal(m.fixed_copy_r(m.fixed_r_const()), m.fixed_r_const())

