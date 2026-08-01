
def test_shift_list():
    assert Poly(x*y, [x,y]).shift_list([1,2]) == Poly((x+1)*(y+2), [x,y])

