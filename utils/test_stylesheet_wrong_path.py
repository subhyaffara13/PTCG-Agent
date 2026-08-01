
def test_stylesheet_wrong_path(geom_df):
    pytest.importorskip("lxml.etree")

    xsl = os.path.join("does", "not", "exist", "row_field_output.xslt")

    with pytest.raises(
        FileNotFoundError, match=r"\[Errno 2\] No such file or director"
    ):
        geom_df.to_xml(stylesheet=xsl)

