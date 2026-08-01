
def test_compressed_suptitle():
    fig, (ax0, ax1) = plt.subplots(
        nrows=2, figsize=(4, 10), layout="compressed",
        gridspec_kw={"height_ratios": (1 / 4, 3 / 4), "hspace": 0})

    ax0.axis("equal")
    ax0.set_box_aspect(1/3)

    ax1.axis("equal")
    ax1.set_box_aspect(1)

    title = fig.suptitle("Title")
    fig.draw_without_rendering()
    assert title.get_position()[1] == pytest.approx(0.7491, abs=1e-3)

    title = fig.suptitle("Title", y=0.98)
    fig.draw_without_rendering()
    assert title.get_position()[1] == 0.98

    title = fig.suptitle("Title", in_layout=False)
    fig.draw_without_rendering()
    assert title.get_position()[1] == 0.98

