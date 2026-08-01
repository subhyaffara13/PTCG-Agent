
def test_Heap():  # `Heap` only supports NumPy backend
    values = np.asarray([2, -1, 0, -1.5, 3])
    heap = Heap(values)

    pair = heap.get_min()
    assert_equal(pair['key'], 3)
    assert_equal(pair['value'], -1.5)

    heap.remove_min()
    pair = heap.get_min()
    assert_equal(pair['key'], 1)
    assert_equal(pair['value'], -1)

    heap.change_value(1, 2.5)
    pair = heap.get_min()
    assert_equal(pair['key'], 2)
    assert_equal(pair['value'], 0)

    heap.remove_min()
    heap.remove_min()

    heap.change_value(1, 10)
    pair = heap.get_min()
    assert_equal(pair['key'], 4)
    assert_equal(pair['value'], 3)

    heap.remove_min()
    pair = heap.get_min()
    assert_equal(pair['key'], 1)
    assert_equal(pair['value'], 10)

