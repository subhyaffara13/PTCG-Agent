
def test_filepath_or_buffer_bad_arg_raises(float_frame, method):
    if method in ["to_latex"]:  # uses styler implementation
        pytest.importorskip("jinja2")
    msg = "buf is not a file name and it has no write method"
    with pytest.raises(TypeError, match=msg):
        getattr(float_frame, method)(buf=object())

