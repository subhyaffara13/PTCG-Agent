
def test_hexagonal_lattice_no_pos():
    # Test positions are note computed/stored when with_positions=False
    G = nx.hexagonal_lattice_graph(6, 6, with_positions=False)
    assert all(pos is None for _, pos in G.nodes(data="pos"))

