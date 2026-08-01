
def test_invalid_file_inputs(request, all_parsers):
    # GH#45957
    parser = all_parsers
    if parser.engine == "python":
        request.applymarker(
            pytest.mark.xfail(reason=f"{parser.engine} engine supports lists.")
        )

    with pytest.raises(ValueError, match="Invalid"):
        parser.read_csv([])

