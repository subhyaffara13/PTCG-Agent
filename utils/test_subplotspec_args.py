
def test_subplotspec_args():
    fig, axs = plt.subplots(1, 2)
    # should work:
    gs = gridspec.GridSpecFromSubplotSpec(2, 1,
                                          subplot_spec=axs[0].get_subplotspec())
    assert gs.get_topmost_subplotspec() == axs[0].get_subplotspec()
    with pytest.raises(TypeError, match="subplot_spec must be type SubplotSpec"):
        gs = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=axs[0])
    with pytest.raises(TypeError, match="subplot_spec must be type SubplotSpec"):
        gs = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=axs)

