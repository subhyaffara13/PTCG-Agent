
def test_scale3d_invalid_keywords_raise():
    """Invalid kwargs should raise TypeError."""
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    with pytest.raises(TypeError):
        ax.set_xscale('log', invalid_kwarg=True)

    with pytest.raises(TypeError):
        ax.set_yscale('symlog', invalid_kwarg=True)

    with pytest.raises(TypeError):
        ax.set_zscale('logit', invalid_kwarg=True)

