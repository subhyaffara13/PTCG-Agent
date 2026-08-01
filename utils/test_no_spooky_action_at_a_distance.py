
def test_no_spooky_action_at_a_distance(cls, xp):
    # test that application of lazy_xp_function to a method which is inherited
    # from a parent class do not propagate to the parent class. Calls to A.g
    # will raise here if A.g was accidentally jitted.
    x = xp.asarray([1.1, 2.2, 3.3])
    y = xp.asarray([1.0, 2.0, 3.0])
    z = xp.asarray([3.0, 4.0, 5.0])
    foo = cls(x)
    observed = foo.g(y, z)
    expected = xp.asarray(44.0)[()]
    xp_assert_close(observed, expected)

