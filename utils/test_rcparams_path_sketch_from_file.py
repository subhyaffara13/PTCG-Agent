
def test_rcparams_path_sketch_from_file(tmp_path, value):
    rc_path = tmp_path / "matplotlibrc"
    rc_path.write_text(f"path.sketch: {value}")
    with mpl.rc_context(fname=rc_path):
        assert mpl.rcParams["path.sketch"] == (1, 2, 3)

