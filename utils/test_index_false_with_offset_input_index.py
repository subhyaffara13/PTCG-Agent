
def test_index_false_with_offset_input_index(parser, typ, geom_df):
    """
    Tests that the output does not contain the `<index>` field when the index of the
    input Dataframe has an offset.

    This is a regression test for issue #42458.
    """

    expected = """\
<?xml version='1.0' encoding='utf-8'?>
<data>
  <row>
    <shape>square</shape>
    <degrees>360</degrees>
    <sides>4.0</sides>
  </row>
  <row>
    <shape>circle</shape>
    <degrees>360</degrees>
    <sides/>
  </row>
  <row>
    <shape>triangle</shape>
    <degrees>180</degrees>
    <sides>3.0</sides>
  </row>
</data>"""
    offset_index = [typ(i) for i in range(10, 13)]
    offset_geom_df = geom_df.copy()
    offset_geom_df.index = Index(offset_index)
    output = offset_geom_df.to_xml(index=False, parser=parser)
    output = equalize_decl(output)

    assert output == expected

