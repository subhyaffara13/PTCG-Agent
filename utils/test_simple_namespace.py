
def test_simple_namespace():
    ns = m.get_simple_namespace()
    assert ns.attr == 42
    assert ns.x == "foo"
    assert ns.right == 2
    assert not hasattr(ns, "wrong")

