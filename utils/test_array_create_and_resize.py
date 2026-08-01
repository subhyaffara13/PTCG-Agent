
def test_array_create_and_resize():
    a = m.create_and_resize(2)
    assert a.size == 4
    assert np.all(a == 42.0)

