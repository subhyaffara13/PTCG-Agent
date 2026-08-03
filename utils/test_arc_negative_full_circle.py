from pathlib import Path


def test_arc_negative_full_circle(theta1, theta2):
    # An exact negative multiple of 360 must draw a complete circle.
    # The result is the same complete circle as the equivalent positive turn
    # starting from *theta1* (so the assertion holds for non-cardinal starts).
    np.testing.assert_allclose(Path.arc(theta1, theta2).vertices,
                               Path.arc(theta1, theta1 + 360).vertices)

