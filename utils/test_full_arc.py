from pathlib import Path


def test_full_arc(offset):
    low = offset
    high = 360 + offset

    path = Path.arc(low, high)
    mins = np.min(path.vertices, axis=0)
    maxs = np.max(path.vertices, axis=0)
    np.testing.assert_allclose(mins, -1)
    np.testing.assert_allclose(maxs, 1)

