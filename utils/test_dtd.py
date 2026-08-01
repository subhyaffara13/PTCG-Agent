
def test_dtd(parser, temp_file):
    xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE non-profits [
    <!ELEMENT shapes (shape*) >
    <!ELEMENT shape ( name, type )>
    <!ELEMENT name (#PCDATA)>
]>
<shapes>
  <shape>
    <name>circle</name>
    <type>2D</type>
  </shape>
  <shape>
    <name>sphere</name>
    <type>3D</type>
  </shape>
</shapes>"""

    df_xpath = read_xml(StringIO(xml), xpath=".//shape", parser=parser)

    df_iter = read_xml_iterparse(
        xml, temp_file, parser=parser, iterparse={"shape": ["name", "type"]}
    )

    df_expected = DataFrame(
        {
            "name": ["circle", "sphere"],
            "type": ["2D", "3D"],
        }
    )

    tm.assert_frame_equal(df_xpath, df_expected)
    tm.assert_frame_equal(df_iter, df_expected)

