
def test_readjson_unicode(request, monkeypatch, engine, temp_file):
    if engine == "pyarrow":
        # GH 48893
        reason = (
            "Pyarrow only supports a file path as an input and line delimited json"
            "and doesn't support chunksize parameter."
        )
        request.applymarker(pytest.mark.xfail(reason=reason, raises=ValueError))

    monkeypatch.setattr("locale.getpreferredencoding", lambda do_setlocale: "cp949")
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write('{"£©µÀÆÖÞßéöÿ":["АБВГДабвгд가"]}')

    result = read_json(temp_file, engine=engine)
    expected = DataFrame({"£©µÀÆÖÞßéöÿ": ["АБВГДабвгд가"]})
    tm.assert_frame_equal(result, expected)

