
def test_default_namespace(parser, geom_df):
    expected = """\
<?xml version='1.0' encoding='utf-8'?>
<data xmlns="http://example.com">
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

    output = geom_df.to_xml(namespaces={"": "http://example.com"}, parser=parser)
    output = equalize_decl(output)

    assert output == expected


def test_default_namespace(parser, temp_file):
    df_nmsp = read_xml(
        StringIO(xml_default_nmsp),
        xpath=".//ns:row",
        namespaces={"ns": "http://example.com"},
        parser=parser,
    )

    df_iter = read_xml_iterparse(
        xml_default_nmsp,
        temp_file,
        parser=parser,
        iterparse={"row": ["shape", "degrees", "sides"]},
    )

    df_expected = DataFrame(
        {
            "shape": ["square", "circle", "triangle"],
            "degrees": [360, 360, 180],
            "sides": [4.0, float("nan"), 3.0],
        }
    )

    tm.assert_frame_equal(df_nmsp, df_expected)
    tm.assert_frame_equal(df_iter, df_expected)

