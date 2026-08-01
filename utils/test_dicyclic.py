
def test_dicyclic(n, axis):
    """Test that the dicyclic group correctly fixes the rotations of a
    prism."""
    P = _generate_prism(n, axis='XYZ'.index(axis))
    for g in Rotation.create_group(f"D{n}", axis=axis):
        assert _calculate_rmsd(P, g.apply(P)) < TOL

