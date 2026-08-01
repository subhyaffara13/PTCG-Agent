
def test_rcparams_legend_loc_from_file(tmp_path, value):
    # rcParams['legend.loc'] should be settable from matplotlibrc.
    # if any of these are not allowed, an exception will be raised.
    # test for gh issue #22338
    rc_path = tmp_path / "matplotlibrc"
    rc_path.write_text(f"legend.loc: {value}")

    with mpl.rc_context(fname=rc_path):
        assert mpl.rcParams["legend.loc"] == value

