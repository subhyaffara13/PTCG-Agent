
def test_elems_and_attrs_cols(parser, geom_df):
    elems_cols_expected = """\
<?xml version='1.0' encoding='utf-8'?>
<data>
  <row shape="square">
    <degrees>360</degrees>
    <sides>4.0</sides>
  </row>
  <row shape="circle">
    <degrees>360</degrees>
    <sides/>
  </row>
  <row shape="triangle">
    <degrees>180</degrees>
    <sides>3.0</sides>
  </row>
</data>"""

    output = geom_df.to_xml(
        index=False,
        elem_cols=["degrees", "sides"],
        attr_cols=["shape"],
        parser=parser,
    )
    output = equalize_decl(output)

    assert output == elems_cols_expected

