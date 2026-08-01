
def test_compression_read(parser, compression_only, tmp_path, temp_file):
    comp_path = tmp_path / "test.xml"
    geom_df.to_xml(comp_path, index=False, parser=parser, compression=compression_only)

    df_xpath = read_xml(comp_path, parser=parser, compression=compression_only)

    df_iter = read_xml_iterparse_comp(
        comp_path,
        compression_only,
        temp_file,
        parser=parser,
        iterparse={"row": ["shape", "degrees", "sides"]},
        compression=compression_only,
    )

    tm.assert_frame_equal(df_xpath, geom_df)
    tm.assert_frame_equal(df_iter, geom_df)

