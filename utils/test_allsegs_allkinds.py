
def test_allsegs_allkinds():
    x, y = np.meshgrid(np.arange(0, 10, 2), np.arange(0, 10, 2))
    z = np.sin(x) * np.cos(y)

    cs = plt.contour(x, y, z, levels=[0, 0.5])

    # Expect two levels, the first with 5 segments and the second with 4.
    for result in [cs.allsegs, cs.allkinds]:
        assert len(result) == 2
        assert len(result[0]) == 5
        assert len(result[1]) == 4

