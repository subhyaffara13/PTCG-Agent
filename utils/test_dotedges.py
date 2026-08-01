
def test_dotedges():
    assert sorted(dotedges(x+2, repeat=False)) == [
        '"Add(Integer(2), Symbol(\'x\'))" -> "Integer(2)";',
        '"Add(Integer(2), Symbol(\'x\'))" -> "Symbol(\'x\')";'
    ]
    assert sorted(dotedges(x + 2, repeat=True)) == [
        '"Add(Integer(2), Symbol(\'x\'))_()" -> "Integer(2)_(0,)";',
        '"Add(Integer(2), Symbol(\'x\'))_()" -> "Symbol(\'x\')_(1,)";'
    ]

