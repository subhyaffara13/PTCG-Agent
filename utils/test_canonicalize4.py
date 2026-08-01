
def test_canonicalize4():
    #Check whether TensAdd.canon_bp chokes on a case where the type of the expression changes on calling expand
    Cartesian = TensorIndexType('Cartesian', dim=3)
    p = tensor_indices("p", Cartesian)
    K = TensorHead("K", [Cartesian])
    expr = TensAdd( K(p) , - 2*K(p) )
    assert expr.canon_bp() == -K(p)

