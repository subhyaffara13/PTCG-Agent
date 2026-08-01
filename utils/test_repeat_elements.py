
def test_repeat_elements(parser, temp_file):
    xml = """\
<shapes>
  <shape>
    <value item="name">circle</value>
    <value item="family">ellipse</value>
    <value item="degrees">360</value>
    <value item="sides">0</value>
  </shape>
  <shape>
    <value item="name">triangle</value>
    <value item="family">polygon</value>
    <value item="degrees">180</value>
    <value item="sides">3</value>
  </shape>
  <shape>
    <value item="name">square</value>
    <value item="family">polygon</value>
    <value item="degrees">360</value>
    <value item="sides">4</value>
  </shape>
</shapes>"""
    df_xpath = read_xml(
        StringIO(xml),
        xpath=".//shape",
        parser=parser,
        names=["name", "family", "degrees", "sides"],
    )

    df_iter = read_xml_iterparse(
        xml,
        temp_file,
        parser=parser,
        iterparse={"shape": ["value", "value", "value", "value"]},
        names=["name", "family", "degrees", "sides"],
    )

    df_expected = DataFrame(
        {
            "name": ["circle", "triangle", "square"],
            "family": ["ellipse", "polygon", "polygon"],
            "degrees": [360, 180, 360],
            "sides": [0, 3, 4],
        }
    )

    tm.assert_frame_equal(df_xpath, df_expected)
    tm.assert_frame_equal(df_iter, df_expected)

