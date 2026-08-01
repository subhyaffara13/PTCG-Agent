
def test_octahedral():
    """Test that the octahedral group correctly fixes the rotations of an
    octahedron."""
    P = _generate_octahedron()
    for g in Rotation.create_group("O"):
        assert _calculate_rmsd(P, g.apply(P)) < TOL


def test_octahedral():
    G = nx.octahedral_graph()
    for flow_func in flow_funcs:
        errmsg = f"Assertion failed in function: {flow_func.__name__}"
        assert 4 == nx.node_connectivity(G, flow_func=flow_func), errmsg
        assert 4 == nx.edge_connectivity(G, flow_func=flow_func), errmsg


def test_octahedral():
    G = nx.octahedral_graph()
    assert 4 == approx.node_connectivity(G)
    assert 4 == approx.node_connectivity(G, 0, 5)

