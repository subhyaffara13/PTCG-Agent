
def test_vectorized_noreturn():
    x = m.NonPODClass(0)
    assert x.value == 0
    m.add_to(x, [1, 2, 3, 4])
    assert x.value == 10
    m.add_to(x, 1)
    assert x.value == 11
    m.add_to(x, [[1, 1], [2, 3]])
    assert x.value == 18

