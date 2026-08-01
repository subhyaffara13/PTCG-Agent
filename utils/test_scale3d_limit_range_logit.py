
def test_scale3d_limit_range_logit():
    """Logit scale should constrain axis to (0, 1)."""
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set(xscale='logit', yscale='logit', zscale='logit',
           xlim=(-0.5, 1.5), ylim=(-0.5, 1.5), zlim=(-0.5, 1.5))

    # Limits should be constrained to (0, 1)
    for name, lim in [('x', ax.get_xlim()), ('y', ax.get_ylim()),
                      ('z', ax.get_zlim())]:
        assert lim[0] > 0, f"{name} lower limit should be > 0 for logit"
        assert lim[1] < 1, f"{name} upper limit should be < 1 for logit"

