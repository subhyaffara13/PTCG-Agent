
def test_icosahedral():
    """The icosahedral group fixes the rotations of an icosahedron. Here we
    test that the icosahedron is invariant after application of the elements
    of the rotation group."""
    P = _generate_icosahedron()
    for g in Rotation.create_group("I"):
        g = Rotation.from_quat(g.as_quat())
        assert _calculate_rmsd(P, g.apply(P)) < TOL


def test_icosahedral():
    G = nx.icosahedral_graph()
    for flow_func in flow_funcs:
        errmsg = f"Assertion failed in function: {flow_func.__name__}"
        assert 5 == nx.node_connectivity(G, flow_func=flow_func), errmsg
        assert 5 == nx.edge_connectivity(G, flow_func=flow_func), errmsg

