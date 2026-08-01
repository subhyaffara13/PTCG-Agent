
def test_attrs_cols_nan_output(parser, geom_df):
    expected = """\
<?xml version='1.0' encoding='utf-8'?>
<data>
  <row index="0" shape="square" degrees="360" sides="4.0"/>
  <row index="1" shape="circle" degrees="360"/>
  <row index="2" shape="triangle" degrees="180" sides="3.0"/>
</data>"""

    output = geom_df.to_xml(attr_cols=["shape", "degrees", "sides"], parser=parser)
    output = equalize_decl(output)

    assert output == expected

