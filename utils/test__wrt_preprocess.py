
def test_Wrt_preprocess():
    assert Wrt.preprocess(x) == ['x']
    assert Wrt.preprocess('') == []
    assert Wrt.preprocess(' ') == []
    assert Wrt.preprocess('x,y') == ['x', 'y']
    assert Wrt.preprocess('x y') == ['x', 'y']
    assert Wrt.preprocess('x, y') == ['x', 'y']
    assert Wrt.preprocess('x , y') == ['x', 'y']
    assert Wrt.preprocess(' x, y') == ['x', 'y']
    assert Wrt.preprocess(' x,  y') == ['x', 'y']
    assert Wrt.preprocess([x, y]) == ['x', 'y']

    raises(OptionError, lambda: Wrt.preprocess(','))
    raises(OptionError, lambda: Wrt.preprocess(0))

