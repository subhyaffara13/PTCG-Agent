
def test_set_figure():
    fig = plt.figure()
    sfig1 = fig.subfigures()
    sfig2 = sfig1.subfigures()

    for f in fig, sfig1, sfig2:
        with pytest.warns(mpl.MatplotlibDeprecationWarning):
            f.set_figure(fig)

    with pytest.raises(ValueError, match="cannot be changed"):
        sfig2.set_figure(sfig1)

    with pytest.raises(ValueError, match="cannot be changed"):
        sfig1.set_figure(plt.figure())

