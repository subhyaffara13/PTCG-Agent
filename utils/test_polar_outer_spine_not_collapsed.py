
def test_polar_outer_spine_not_collapsed(theta_zero_location, theta_offset):
    # The polar outer spine spans a full turn via Path.arc.  For some theta
    # offsets/directions, floating-point error left the span just short of a
    # full 360 degrees and the spine collapsed to a near-empty arc.  Check it
    # still occupies a sensible area.
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    if theta_zero_location is not None:
        ax.set_theta_direction(-1)
        ax.set_theta_zero_location(*theta_zero_location)
    if theta_offset is not None:
        ax.set_theta_offset(theta_offset)
    fig.canvas.draw()
    # A collapsed spine has a near-zero (~1e-13) bounding box; a healthy one is
    # hundreds of points across.
    assert ax.spines['polar'].get_tightbbox().size.min() > 1

