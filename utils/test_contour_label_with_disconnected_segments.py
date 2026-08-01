
def test_contour_label_with_disconnected_segments():
    x, y = np.mgrid[-1:1:21j, -1:1:21j]
    z = 1 / np.sqrt(0.01 + (x + 0.3) ** 2 + y ** 2)
    z += 1 / np.sqrt(0.01 + (x - 0.3) ** 2 + y ** 2)

    plt.figure()
    cs = plt.contour(x, y, z, levels=[7])
    cs.clabel(manual=[(0.2, 0.1)])

