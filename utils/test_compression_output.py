
def test_compression_output(parser, compression_only, geom_df, temp_file):
    path = temp_file
    geom_df.to_xml(path, parser=parser, compression=compression_only)

    with get_handle(
        path,
        "r",
        compression=compression_only,
    ) as handle_obj:
        output = handle_obj.handle.read()

    output = equalize_decl(output)

    assert geom_xml == output.strip()

