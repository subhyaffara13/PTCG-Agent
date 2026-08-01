
def test_double_2():
    assert ae(quadts(lambda x, y: (x-1)/((1-x*y)*log(x*y)), [0, 1], [0, 1]), euler)

