
def test_unused_namespaces(parser, geom_df):
    expected = """\
<?xml version='1.0' encoding='utf-8'?>
<data xmlns:oth="http://other.org" xmlns:ex="http://example.com">
  <row>
    <index>0</index>
    <shape>square</shape>
    <degrees>360</degrees>
    <sides>4.0</sides>
  </row>
  <row>
    <index>1</index>
    <shape>circle</shape>
    <degrees>360</degrees>
    <sides/>
  </row>
  <row>
    <index>2</index>
    <shape>triangle</shape>
    <degrees>180</degrees>
    <sides>3.0</sides>
  </row>
</data>"""

    output = geom_df.to_xml(
        namespaces={"oth": "http://other.org", "ex": "http://example.com"},
        parser=parser,
    )
    output = equalize_decl(output)

    assert output == expected

