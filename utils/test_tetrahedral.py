
def test_tetrahedral():
    """Test that the tetrahedral group correctly fixes the rotations of a
    tetrahedron."""
    P = _generate_tetrahedron()
    for g in Rotation.create_group("T"):
        assert _calculate_rmsd(P, g.apply(P)) < TOL


def test_tetrahedral():
    # Actual coefficient is 1
    G = nx.tetrahedral_graph()
    assert average_clustering(G, trials=len(G) // 2) == nx.average_clustering(G)

