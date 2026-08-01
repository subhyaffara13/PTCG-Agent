
def test_immutability():
    with raises(TypeError):
        IM[2, 2] = 5
    with raises(TypeError):
        ISM[2, 2] = 5

