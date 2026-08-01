
def test_scale3d_keywords_accepted(scale_type, kwargs):
    """Verify that scale keywords are accepted on all 3 axes."""
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for setter in [ax.set_xscale, ax.set_yscale, ax.set_zscale]:
        setter(scale_type, **kwargs)
    assert (ax.get_xscale(), ax.get_yscale(), ax.get_zscale()) == (scale_type,) * 3

