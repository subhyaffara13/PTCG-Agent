
def test_attrs_cols_prefix(parser, geom_df):
    expected = """\
<?xml version='1.0' encoding='utf-8'?>
<doc:data xmlns:doc="http://example.xom">
  <doc:row doc:index="0" doc:shape="square" \
doc:degrees="360" doc:sides="4.0"/>
  <doc:row doc:index="1" doc:shape="circle" \
doc:degrees="360"/>
  <doc:row doc:index="2" doc:shape="triangle" \
doc:degrees="180" doc:sides="3.0"/>
</doc:data>"""

    output = geom_df.to_xml(
        attr_cols=["index", "shape", "degrees", "sides"],
        namespaces={"doc": "http://example.xom"},
        prefix="doc",
        parser=parser,
    )
    output = equalize_decl(output)

    assert output == expected

