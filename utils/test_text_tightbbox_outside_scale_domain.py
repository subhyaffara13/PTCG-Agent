
def test_text_tightbbox_outside_scale_domain():
    # Test that text at positions outside the valid domain of axes scales
    # (e.g., negative coordinates with log scale) returns a null bbox.
    fig, ax = plt.subplots()
    ax.set_yscale('log')
    ax.set_ylim(1, 100)

    invalid_text = ax.text(0, -5, 'invalid')
    invalid_bbox = invalid_text.get_tightbbox(fig.canvas.get_renderer())
    assert not np.isfinite(invalid_bbox.width)

