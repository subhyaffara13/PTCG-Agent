
def test_filepath_or_buffer_arg(
    method,
    tmp_path,
    encoding,
    data,
    filepath_or_buffer_id,
):
    if filepath_or_buffer_id == "buffer":
        filepath_or_buffer = StringIO()
    elif filepath_or_buffer_id == "pathlike":
        filepath_or_buffer = tmp_path / "foo"
    else:
        filepath_or_buffer = str(tmp_path / "foo")

    df = DataFrame([data])
    if method in ["to_latex"]:  # uses styler implementation
        pytest.importorskip("jinja2")

    if filepath_or_buffer_id not in ["string", "pathlike"] and encoding is not None:
        with pytest.raises(
            ValueError, match="buf is not a file name and encoding is specified."
        ):
            getattr(df, method)(buf=filepath_or_buffer, encoding=encoding)
    elif encoding == "foo":
        with pytest.raises(LookupError, match="unknown encoding"):
            getattr(df, method)(buf=filepath_or_buffer, encoding=encoding)
    else:
        expected = getattr(df, method)()
        getattr(df, method)(buf=filepath_or_buffer, encoding=encoding)
        encoding = encoding or "utf-8"
        if filepath_or_buffer_id == "string":
            with open(filepath_or_buffer, encoding=encoding) as f:
                result = f.read()
        elif filepath_or_buffer_id == "pathlike":
            result = filepath_or_buffer.read_text(encoding=encoding)
        elif filepath_or_buffer_id == "buffer":
            result = filepath_or_buffer.getvalue()
        assert result == expected
    if filepath_or_buffer_id == "buffer":
        assert not filepath_or_buffer.closed

