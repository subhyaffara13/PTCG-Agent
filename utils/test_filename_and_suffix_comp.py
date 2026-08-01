
def test_filename_and_suffix_comp(
    parser, compression_only, geom_df, compression_to_extension, tmp_path
):
    compfile = "xml." + compression_to_extension[compression_only]
    path = tmp_path / compfile
    geom_df.to_xml(path, parser=parser, compression=compression_only)

    with get_handle(
        path,
        "r",
        compression=compression_only,
    ) as handle_obj:
        output = handle_obj.handle.read()

    output = equalize_decl(output)

    assert geom_xml == output.strip()

