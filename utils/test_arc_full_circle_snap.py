
def test_arc_full_circle_snap(theta2):
    # A span within floating-point tolerance of a whole number of turns must
    # draw a complete circle, not collapse to a near-empty arc.
    np.testing.assert_allclose(Path.arc(0, theta2).vertices,
                               Path.arc(0, 360).vertices)

