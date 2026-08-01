
def test_figaspect():
    w, h = plt.figaspect(np.float64(2) / np.float64(1))
    assert h / w == 2
    w, h = plt.figaspect(2)
    assert h / w == 2
    w, h = plt.figaspect(np.zeros((1, 2)))
    assert h / w == 0.5
    w, h = plt.figaspect(np.zeros((2, 2)))
    assert h / w == 1

