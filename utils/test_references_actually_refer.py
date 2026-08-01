
def test_references_actually_refer(m):
    a = m.reference_tensor()
    temp = a[indices]
    a[indices] = 100
    assert_equal_tensor_ref(m.copy_const_tensor(), modified=100)
    a[indices] = temp
    assert_equal_tensor_ref(m.copy_const_tensor())

    a = m.reference_view_of_tensor()
    a[indices] = 100
    assert_equal_tensor_ref(m.copy_const_tensor(), modified=100)
    a[indices] = temp
    assert_equal_tensor_ref(m.copy_const_tensor())

