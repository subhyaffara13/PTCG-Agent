
def test_Return():
    rs = Return(x)
    assert rs.args == (x,)
    assert rs == Return(x)
    assert rs != Return(y)
    assert rs.func(*rs.args) == rs

