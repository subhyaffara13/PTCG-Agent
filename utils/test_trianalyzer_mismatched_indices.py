
def test_trianalyzer_mismatched_indices():
    # github issue 4999.
    x = np.array([0., 1., 0.5, 0., 2.])
    y = np.array([0., 0., 0.5*np.sqrt(3.), -1., 1.])
    triangles = np.array([[0, 1, 2], [0, 1, 3], [1, 2, 4]], dtype=np.int32)
    mask = np.array([False, False, True], dtype=bool)
    triang = mtri.Triangulation(x, y, triangles, mask=mask)
    analyser = mtri.TriAnalyzer(triang)
    # numpy >= 1.10 raises a VisibleDeprecationWarning in the following line
    # prior to the fix.
    analyser._get_compressed_triangulation()

