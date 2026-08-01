
def test_respects_bbox():
    fig, axs = plt.subplots(2)
    for ax in axs:
        ax.set_axis_off()
    im = axs[1].imshow([[0, 1], [2, 3]], aspect="auto", extent=(0, 1, 0, 1))
    im.set_clip_path(None)
    # Make the image invisible in axs[1], but visible in axs[0] if we pan
    # axs[1] up.
    im.set_clip_box(axs[0].bbox)
    buf_before = io.BytesIO()
    fig.savefig(buf_before, format="rgba")
    assert {*buf_before.getvalue()} == {0xff}  # All white.
    axs[1].set(ylim=(-1, 0))
    buf_after = io.BytesIO()
    fig.savefig(buf_after, format="rgba")
    assert buf_before.getvalue() != buf_after.getvalue()  # Not all white.

