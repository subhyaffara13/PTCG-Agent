
def test_infer_compression(all_parsers, csv1, buffer, ext):
    # see gh-9770
    parser = all_parsers
    kwargs = {"index_col": 0, "parse_dates": True}

    expected = parser.read_csv(csv1, **kwargs)
    kwargs["compression"] = "infer"

    if buffer:
        with open(csv1, encoding="utf-8") as f:
            result = parser.read_csv(f, **kwargs)
    else:
        ext = "." + ext if ext else ""
        result = parser.read_csv(csv1 + ext, **kwargs)

    tm.assert_frame_equal(result, expected)

