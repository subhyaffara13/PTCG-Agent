
def test_str_norms(fig_test, fig_ref):
    t = np.random.rand(10, 10) * .8 + .1  # between 0 and 1
    axts = fig_test.subplots(1, 5)
    axts[0].imshow(t, norm="log")
    axts[1].imshow(t, norm="log", vmin=.2)
    axts[2].imshow(t, norm="symlog")
    axts[3].imshow(t, norm="symlog", vmin=.3, vmax=.7)
    axts[4].imshow(t, norm="logit", vmin=.3, vmax=.7)
    axrs = fig_ref.subplots(1, 5)
    axrs[0].imshow(t, norm=colors.LogNorm())
    axrs[1].imshow(t, norm=colors.LogNorm(vmin=.2))
    # same linthresh as SymmetricalLogScale's default.
    axrs[2].imshow(t, norm=colors.SymLogNorm(linthresh=2))
    axrs[3].imshow(t, norm=colors.SymLogNorm(linthresh=2, vmin=.3, vmax=.7))
    axrs[4].imshow(t, norm="logit", clim=(.3, .7))

    assert type(axts[0].images[0].norm) is colors.LogNorm  # Exactly that class
    with pytest.raises(ValueError):
        axts[0].imshow(t, norm="foobar")

