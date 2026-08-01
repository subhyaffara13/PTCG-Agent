
def test_get_constrained_layout_pads():
    params = {'w_pad': 0.01, 'h_pad': 0.02, 'wspace': 0.03, 'hspace': 0.04}
    expected = tuple([*params.values()])
    fig = plt.figure(layout=mpl.layout_engine.ConstrainedLayoutEngine(**params))
    with pytest.warns(PendingDeprecationWarning, match="will be deprecated"):
        assert fig.get_constrained_layout_pads() == expected

