
def test_contract_metric5():
    R3 = TensorIndexType('R3', dim=3)
    p, q, r = tensor_indices("p q r", R3)
    delta = R3.delta
    K = TensorHead("K", [R3])

    F = Function("F")
    x = Symbol("x")

    #Check if contract_metric gets into an infinite loop when given a TensMul whose coeff is an Add
    expr = (2+F(x))*K(-p)*K(-q)
    assert expr.contract_metric(delta) == expr

