
def test_operator_inv():
    A = Operator('A')
    assert A*A.inv() == 1
    assert A.inv()*A == 1

