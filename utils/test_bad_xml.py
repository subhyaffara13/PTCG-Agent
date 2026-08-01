
def test_bad_xml(parser, temp_file):
    bad_xml = """\
<?xml version='1.0' encoding='utf-8'?>
  <row>
    <shape>square</shape>
    <degrees>00360</degrees>
    <sides>4.0</sides>
    <date>2020-01-01</date>
   </row>
  <row>
    <shape>circle</shape>
    <degrees>00360</degrees>
    <sides/>
    <date>2021-01-01</date>
  </row>
  <row>
    <shape>triangle</shape>
    <degrees>00180</degrees>
    <sides>3.0</sides>
    <date>2022-01-01</date>
  </row>
"""
    temp_file.write_text(bad_xml, encoding="utf-8")

    with pytest.raises(
        SyntaxError,
        match="Extra content at the end of the document|junk after document element",
    ):
        read_xml(
            temp_file,
            parser=parser,
            parse_dates=["date"],
            iterparse={"row": ["shape", "degrees", "sides", "date"]},
        )

