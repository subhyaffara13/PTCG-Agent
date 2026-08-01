
def test_2d_to_rgba():
    color = np.array([0.1, 0.2, 0.3])
    rgba_1d = mcolors.to_rgba(color.reshape(-1))
    rgba_2d = mcolors.to_rgba(color.reshape((1, -1)))
    assert rgba_1d == rgba_2d

