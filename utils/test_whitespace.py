
def test_whitespace(parser, temp_file):
    xml = """
      <data>
        <row sides=" 4 ">
          <shape>
              square
          </shape>
          <degrees>&#009;360&#009;</degrees>
        </row>
        <row sides=" 0 ">
          <shape>
              circle
          </shape>
          <degrees>&#009;360&#009;</degrees>
        </row>
        <row sides=" 3 ">
          <shape>
              triangle
          </shape>
          <degrees>&#009;180&#009;</degrees>
        </row>
      </data>"""

    df_xpath = read_xml(StringIO(xml), parser=parser, dtype="string")

    df_iter = read_xml_iterparse(
        xml,
        temp_file,
        parser=parser,
        iterparse={"row": ["sides", "shape", "degrees"]},
        dtype="string",
    )

    df_expected = DataFrame(
        {
            "sides": [" 4 ", " 0 ", " 3 "],
            "shape": [
                "\n              square\n          ",
                "\n              circle\n          ",
                "\n              triangle\n          ",
            ],
            "degrees": ["\t360\t", "\t360\t", "\t180\t"],
        },
        dtype="string",
    )

    tm.assert_frame_equal(df_xpath, df_expected)
    tm.assert_frame_equal(df_iter, df_expected)

