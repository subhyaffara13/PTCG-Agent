
def test_bar_uint8():
    xs = [0, 1, 2, 3]
    b = plt.bar(np.array(xs, dtype=np.uint8), [2, 3, 4, 5], align="edge")
    for (patch, x) in zip(b.patches, xs):
        assert patch.xy[0] == x

