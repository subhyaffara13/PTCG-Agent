
def test_postprocessor():
    """
    Test if substituting a Tensor into a Mul or Add automatically converts it
    to TensMul or TensAdd respectively. See github issue #25051
    """
    R3 = TensorIndexType('R3', dim=3)
    i = tensor_indices("i", R3)
    K = TensorHead("K", [R3])
    x,y,z = symbols("x y z")

    assert isinstance((x*2).xreplace({x: K(i)}), TensMul)
    assert isinstance((x+2).xreplace({x: K(i)*K(-i)}), TensAdd)

    assert isinstance((x*2).subs({x: K(i)}), TensMul)
    assert isinstance((x+2).subs({x: K(i)*K(-i)}), TensAdd)

    assert isinstance((x*2).replace(x, K(i)), TensMul)
    assert isinstance((x+2).replace(x, K(i)*K(-i)), TensAdd)

