
def test_contract_delta2():
    R3 = TensorIndexType('R3', dim=3)
    p, q = tensor_indices("p q", R3)
    delta = R3.delta
    K = TensorHead("K", [R3])

    #Check if TensAdd.contract_delta can handle the case when the TensAdd has non-TensExpr args.
    expr = 1 + K(p)*K(q)*delta(-p,-q)
    assert expr.contract_delta(delta) == 1 + K(p)*K(-p)

