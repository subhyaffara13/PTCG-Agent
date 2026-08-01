
def test_gridspec_no_mutate_input():
    gs = {'left': .1}
    gs_orig = dict(gs)
    plt.subplots(1, 2, width_ratios=[1, 2], gridspec_kw=gs)
    assert gs == gs_orig
    plt.subplot_mosaic('AB', width_ratios=[1, 2], gridspec_kw=gs)

