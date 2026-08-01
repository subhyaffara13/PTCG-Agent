
def test_juxt_generator_input():
    data = list(range(10))
    juxtfunc = juxt(itemgetter(2*i) for i in range(5))
    assert juxtfunc(data) == (0, 2, 4, 6, 8)
    assert juxtfunc(data) == (0, 2, 4, 6, 8)

