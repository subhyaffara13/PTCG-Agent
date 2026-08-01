
def test_fixed():
    assert_equal_ref(m.fixed_c())
    assert_equal_ref(m.fixed_r())
    assert_equal_ref(m.fixed_copy_r(m.fixed_r()))
    assert_equal_ref(m.fixed_copy_c(m.fixed_c()))
    assert_equal_ref(m.fixed_copy_r(m.fixed_c()))
    assert_equal_ref(m.fixed_copy_c(m.fixed_r()))

