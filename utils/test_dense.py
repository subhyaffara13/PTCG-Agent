
def test_dense():
    assert_equal_ref(m.dense_r())
    assert_equal_ref(m.dense_c())
    assert_equal_ref(m.dense_copy_r(m.dense_r()))
    assert_equal_ref(m.dense_copy_c(m.dense_c()))
    assert_equal_ref(m.dense_copy_r(m.dense_c()))
    assert_equal_ref(m.dense_copy_c(m.dense_r()))

