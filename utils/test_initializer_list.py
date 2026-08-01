
def test_initializer_list():
    assert m.array_initializer_list1().shape == (1,)
    assert m.array_initializer_list2().shape == (1, 2)
    assert m.array_initializer_list3().shape == (1, 2, 3)
    assert m.array_initializer_list4().shape == (1, 2, 3, 4)

