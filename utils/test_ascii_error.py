
def test_ascii_error(temp_file, version):
    # GH #61583
    # Check that 2 byte long unicode characters doesn't cause export error
    df = DataFrame({"doubleByteCol": ["§" * 1500]})
    df.to_stata(temp_file, write_index=0, version=version)
    df_input = read_stata(temp_file)
    tm.assert_frame_equal(df, df_input)

