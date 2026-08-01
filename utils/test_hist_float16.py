
def test_hist_float16():
    np.random.seed(19680801)
    values = np.clip(
        np.random.normal(0.5, 0.3, size=1000), 0, 1).astype(np.float16)
    h = plt.hist(values, bins=3, alpha=0.5)
    bc = h[2]
    # Check that there are no overlapping rectangles
    for r in range(1, len(bc)):
        rleft = bc[r-1].get_corners()
        rright = bc[r].get_corners()
        # right hand position of left rectangle <=
        # left hand position of right rectangle
        assert rleft[1][0] <= rright[0][0]

