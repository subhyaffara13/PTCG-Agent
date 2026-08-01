
def test_ANFform():
    x, y = symbols('x,y')
    assert ANFform([x], [1, 1]) == True
    assert ANFform([x], [0, 0]) == False
    assert ANFform([x], [1, 0]) == Xor(x, True, remove_true=False)
    assert ANFform([x, y], [1, 1, 1, 0]) == \
           Xor(True, And(x, y), remove_true=False)

