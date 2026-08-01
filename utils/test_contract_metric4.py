
def test_contract_metric4():
    R3 = TensorIndexType('R3', dim=3)
    p, q, r = tensor_indices("p q r", R3)
    delta = R3.delta
    eps = R3.epsilon
    K = TensorHead("K", [R3])

    #Check whether contract_metric chokes on an expandable expression which becomes zero on canonicalization (issue #24354)
    expr = eps(p,q,r)*( K(-p)*K(-q) + delta(-p,-q) )
    assert expr.contract_metric(delta) == 0

