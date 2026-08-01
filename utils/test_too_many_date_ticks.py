
def test_too_many_date_ticks(caplog):
    # Attempt to test SF 2715172, see
    # https://sourceforge.net/tracker/?func=detail&aid=2715172&group_id=80706&atid=560720
    # setting equal datetimes triggers and expander call in
    # transforms.nonsingular which results in too many ticks in the
    # DayLocator.  This should emit a log at WARNING level.
    caplog.set_level("WARNING")
    t0 = datetime.datetime(2000, 1, 20)
    tf = datetime.datetime(2000, 1, 20)
    fig, ax = plt.subplots()
    with pytest.warns(UserWarning) as rec:
        ax.set_xlim(t0, tf, auto=True)
        assert len(rec) == 1
        assert ('Attempting to set identical low and high xlims'
                in str(rec[0].message))
    ax.plot([], [])
    ax.xaxis.set_major_locator(mdates.DayLocator())
    v = ax.xaxis.get_major_locator()()
    assert len(v) > 1000
    # The warning is emitted multiple times because the major locator is also
    # called both when placing the minor ticks (for overstriking detection) and
    # during tick label positioning.
    assert caplog.records and all(
        record.name == "matplotlib.ticker" and record.levelname == "WARNING"
        for record in caplog.records)
    assert len(caplog.records) > 0

