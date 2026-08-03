import copy

def test_round_trip_references_actually_refer(m):
    # Need to create a copy that matches the type on the C side
    copy = np.array(tensor_ref, dtype=np.float64, order=m.needed_options)
    a = m.round_trip_view_tensor(copy)
    temp = a[indices]
    a[indices] = 100
    assert_equal_tensor_ref(copy, modified=100)
    a[indices] = temp
    assert_equal_tensor_ref(copy)

