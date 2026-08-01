
def test_invalid_layouts():
    fig, ax = plt.subplots(layout="constrained")
    with pytest.warns(UserWarning):
        # this should warn,
        fig.subplots_adjust(top=0.8)
    assert isinstance(fig.get_layout_engine(), ConstrainedLayoutEngine)

    # Using layout + (tight|constrained)_layout warns, but the former takes
    # precedence.
    wst = "The Figure parameters 'layout' and 'tight_layout'"
    with pytest.warns(UserWarning, match=wst):
        fig = Figure(layout='tight', tight_layout=False)
    assert isinstance(fig.get_layout_engine(), TightLayoutEngine)
    wst = "The Figure parameters 'layout' and 'constrained_layout'"
    with pytest.warns(UserWarning, match=wst):
        fig = Figure(layout='constrained', constrained_layout=False)
    assert not isinstance(fig.get_layout_engine(), TightLayoutEngine)
    assert isinstance(fig.get_layout_engine(), ConstrainedLayoutEngine)

    with pytest.raises(ValueError,
                       match="Invalid value for 'layout'"):
        Figure(layout='foobar')

    # test that layouts can be swapped if no colorbar:
    fig, ax = plt.subplots(layout="constrained")
    fig.set_layout_engine("tight")
    assert isinstance(fig.get_layout_engine(), TightLayoutEngine)
    fig.set_layout_engine("constrained")
    assert isinstance(fig.get_layout_engine(), ConstrainedLayoutEngine)

    # test that layouts cannot be swapped if there is a colorbar:
    fig, ax = plt.subplots(layout="constrained")
    pc = ax.pcolormesh(np.random.randn(2, 2))
    fig.colorbar(pc)
    with pytest.raises(RuntimeError, match='Colorbar layout of new layout'):
        fig.set_layout_engine("tight")
    fig.set_layout_engine("none")
    with pytest.raises(RuntimeError, match='Colorbar layout of new layout'):
        fig.set_layout_engine("tight")

    fig, ax = plt.subplots(layout="tight")
    pc = ax.pcolormesh(np.random.randn(2, 2))
    fig.colorbar(pc)
    with pytest.raises(RuntimeError, match='Colorbar layout of new layout'):
        fig.set_layout_engine("constrained")
    fig.set_layout_engine("none")
    assert isinstance(fig.get_layout_engine(), PlaceHolderLayoutEngine)

    with pytest.raises(RuntimeError, match='Colorbar layout of new layout'):
        fig.set_layout_engine("constrained")

