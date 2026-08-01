
def test_namespace_prefix_and_default(parser, geom_df):
    expected = """\
<?xml version='1.0' encoding='utf-8'?>
<doc:data xmlns:doc="http://other.org" xmlns="http://example.com">
  <doc:row>
    <doc:index>0</doc:index>
    <doc:shape>square</doc:shape>
    <doc:degrees>360</doc:degrees>
    <doc:sides>4.0</doc:sides>
  </doc:row>
  <doc:row>
    <doc:index>1</doc:index>
    <doc:shape>circle</doc:shape>
    <doc:degrees>360</doc:degrees>
    <doc:sides/>
  </doc:row>
  <doc:row>
    <doc:index>2</doc:index>
    <doc:shape>triangle</doc:shape>
    <doc:degrees>180</doc:degrees>
    <doc:sides>3.0</doc:sides>
  </doc:row>
</doc:data>"""

    output = geom_df.to_xml(
        namespaces={"": "http://example.com", "doc": "http://other.org"},
        prefix="doc",
        parser=parser,
    )
    output = equalize_decl(output)

    assert output == expected

