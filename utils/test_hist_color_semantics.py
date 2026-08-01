
def test_hist_color_semantics(kwargs, patch_face, patch_edge):
    _, _, patches = plt.figure().subplots().hist([1, 2, 3], **kwargs)
    assert all(mcolors.same_color([p.get_facecolor(), p.get_edgecolor()],
                                  [patch_face, patch_edge]) for p in patches)

