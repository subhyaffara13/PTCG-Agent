
def test_2D_lattice_no_contraction_leftovers(lattice_graph):
    """hexagonal_lattice_graph and triangular_lattice_graph use nx.contracted_nodes
    under-the-hood when periodic=True. Check that there are no leftover
    "contraction" node attributes on the returned graph."""
    G = lattice_graph(6, 6, with_positions=False, periodic=True)
    assert all(data == {} for _, data in G.nodes(data=True))
    assert all(data == {} for _, _, data in G.edges(data=True))

