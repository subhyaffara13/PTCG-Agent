
def test_empty_attribute():
    """Tests that a GraphML string with an empty attribute can be parsed
    correctly."""
    s = """<?xml version='1.0' encoding='utf-8'?>
    <graphml>
      <key id="d1" for="node" attr.name="foo" attr.type="string"/>
      <key id="d2" for="node" attr.name="bar" attr.type="string"/>
      <graph>
        <node id="0">
          <data key="d1">aaa</data>
          <data key="d2">bbb</data>
        </node>
        <node id="1">
          <data key="d1">ccc</data>
          <data key="d2"></data>
        </node>
      </graph>
    </graphml>"""
    fh = io.BytesIO(s.encode("UTF-8"))
    G = nx.read_graphml(fh)
    assert G.nodes["0"] == {"foo": "aaa", "bar": "bbb"}
    assert G.nodes["1"] == {"foo": "ccc", "bar": ""}

