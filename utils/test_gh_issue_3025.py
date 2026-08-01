
def test_gh_issue_3025(xp):
    """Github issue #3025 - improper merging of labels"""
    d = np.zeros((60, 320))
    d[:, :257] = 1
    d[:, 260:] = 1
    d[36, 257] = 1
    d[35, 258] = 1
    d[35, 259] = 1
    d = xp.asarray(d)
    assert ndimage.label(d, xp.ones((3, 3)))[1] == 1

