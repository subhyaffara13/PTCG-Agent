
def test_day_first_parse_dates(parser, temp_file):
    xml = """\
<?xml version='1.0' encoding='utf-8'?>
<data>
  <row>
    <shape>square</shape>
    <degrees>00360</degrees>
    <sides>4.0</sides>
    <date>31/12/2020</date>
   </row>
  <row>
    <shape>circle</shape>
    <degrees>00360</degrees>
    <sides/>
    <date>31/12/2021</date>
  </row>
  <row>
    <shape>triangle</shape>
    <degrees>00180</degrees>
    <sides>3.0</sides>
    <date>31/12/2022</date>
  </row>
</data>"""

    df_expected = DataFrame(
        {
            "shape": ["square", "circle", "triangle"],
            "degrees": [360, 360, 180],
            "sides": [4.0, float("nan"), 3.0],
            "date": to_datetime(["2020-12-31", "2021-12-31", "2022-12-31"]),
        }
    )

    with tm.assert_produces_warning(
        UserWarning, match="Parsing dates in %d/%m/%Y format"
    ):
        df_result = read_xml(StringIO(xml), parse_dates=["date"], parser=parser)
        df_iter = read_xml_iterparse(
            xml,
            parse_dates=["date"],
            parser=parser,
            iterparse={"row": ["shape", "degrees", "sides", "date"]},
            temp_file=temp_file,
        )

        tm.assert_frame_equal(df_result, df_expected)
        tm.assert_frame_equal(df_iter, df_expected)

