
def test_dtype_nullable_int(parser, temp_file):
    df_result = read_xml(StringIO(xml_types), dtype={"sides": "Int64"}, parser=parser)
    df_iter = read_xml_iterparse(
        xml_types,
        parser=parser,
        dtype={"sides": "Int64"},
        iterparse={"row": ["shape", "degrees", "sides"]},
        temp_file=temp_file,
    )

    df_expected = DataFrame(
        {
            "shape": ["square", "circle", "triangle"],
            "degrees": [360, 360, 180],
            "sides": Series([4.0, NA, 3.0], dtype="Int64"),
        }
    )

    tm.assert_frame_equal(df_result, df_expected)
    tm.assert_frame_equal(df_iter, df_expected)

