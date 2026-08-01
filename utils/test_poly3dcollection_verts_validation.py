
def test_poly3dcollection_verts_validation():
    poly = [[0, 0, 1], [0, 1, 1], [0, 1, 0], [0, 0, 0]]
    with pytest.raises(ValueError, match=r'list of \(N, 3\) array-like'):
        art3d.Poly3DCollection(poly)  # should be Poly3DCollection([poly])

    poly = np.array(poly, dtype=float)
    with pytest.raises(ValueError, match=r'shape \(M, N, 3\)'):
        art3d.Poly3DCollection(poly)  # should be Poly3DCollection([poly])

