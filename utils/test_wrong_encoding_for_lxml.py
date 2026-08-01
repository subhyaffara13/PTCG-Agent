
def test_wrong_encoding_for_lxml():
    pytest.importorskip("lxml")
    # GH#45133
    data = """<data>
  <row>
    <a>c</a>
  </row>
</data>
"""
    with pytest.raises(TypeError, match="encoding None"):
        read_xml(StringIO(data), parser="lxml", encoding=None)

