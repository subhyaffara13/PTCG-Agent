
def test_engformatter_offset_oom(
    data_offset,
    noise,
    oom_center_desired,
    oom_noise_desired
):
    UNIT = "eV"
    fig, ax = plt.subplots()
    ydata = data_offset + np.arange(-5, 7, dtype=float)*noise
    ax.plot(ydata)
    formatter = mticker.EngFormatter(useOffset=True, unit=UNIT)
    # So that offset strings will always have the same size
    formatter.ENG_PREFIXES[0] = "_"
    ax.yaxis.set_major_formatter(formatter)
    fig.canvas.draw()
    offset_got = formatter.get_offset()
    ticks_got = [labl.get_text() for labl in ax.get_yticklabels()]
    # Predicting whether offset should be 0 or not is essentially testing
    # ScalarFormatter._compute_offset . This function is pretty complex and it
    # would be nice to test it, but this is out of scope for this test which
    # only makes sure that offset text and the ticks gets the correct unit
    # prefixes and the ticks.
    if formatter.offset:
        prefix_noise_got = offset_got[2]
        prefix_noise_desired = formatter.ENG_PREFIXES[oom_noise_desired]
        prefix_center_got = offset_got[-1-len(UNIT)]
        prefix_center_desired = formatter.ENG_PREFIXES[oom_center_desired]
        assert prefix_noise_desired == prefix_noise_got
        assert prefix_center_desired == prefix_center_got
        # Make sure the ticks didn't get the UNIT
        for tick in ticks_got:
            assert UNIT not in tick
    else:
        assert oom_center_desired == 0
        assert offset_got == ""
        # Make sure the ticks contain now the prefixes
        for tick in ticks_got:
            # 0 is zero on all orders of magnitudes, no matter what is
            # oom_noise_desired
            prefix_idx = 0 if tick[0] == "0" else oom_noise_desired
            assert tick.endswith(formatter.ENG_PREFIXES[prefix_idx] + UNIT)

