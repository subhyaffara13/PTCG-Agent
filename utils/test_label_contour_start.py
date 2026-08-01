
def test_label_contour_start():
    # Set up data and figure/axes that result in automatic labelling adding the
    # label to the start of a contour

    _, ax = plt.subplots(dpi=100)
    lats = lons = np.linspace(-np.pi / 2, np.pi / 2, 50)
    lons, lats = np.meshgrid(lons, lats)
    wave = 0.75 * (np.sin(2 * lats) ** 8) * np.cos(4 * lons)
    mean = 0.5 * np.cos(2 * lats) * ((np.sin(2 * lats)) ** 2 + 2)
    data = wave + mean

    cs = ax.contour(lons, lats, data)

    with mock.patch.object(
            cs, '_split_path_and_get_label_rotation',
            wraps=cs._split_path_and_get_label_rotation) as mocked_splitter:
        # Smoke test that we can add the labels
        cs.clabel(fontsize=9)

    # Verify at least one label was added to the start of a contour.  I.e. the
    # splitting method was called with idx=0 at least once.
    idxs = [cargs[0][1] for cargs in mocked_splitter.call_args_list]
    assert 0 in idxs

