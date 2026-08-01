
def test_Node():
    n = Node()
    assert n == Node()
    assert n.func(*n.args) == n

