
def test_arc_unwrap_partial_turn():
    # A span comfortably more than a whole number of turns (not near-integer)
    # is unwrapped to the equivalent shortest arc within 360 degrees.
    np.testing.assert_allclose(Path.arc(0, 410).vertices,
                               Path.arc(0, 50).vertices)
    np.testing.assert_allclose(Path.arc(0, 540).vertices,
                               Path.arc(0, 180).vertices)
    # A span a clear fraction of a degree past a full turn is the caller's
    # explicit request and must NOT be snapped to a circle (tolerance guard).
    np.testing.assert_allclose(Path.arc(0, 360.001).vertices,
                               Path.arc(0, 0.001).vertices)

