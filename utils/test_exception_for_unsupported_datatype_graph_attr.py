
def test_exception_for_unsupported_datatype_graph_attr():
    """Test that a detailed exception is raised when an attribute is of a type
    not supported by GraphML, e.g. a list"""
    pytest.importorskip("lxml.etree")
    # graph attribute
    G = nx.Graph()
    G.graph["my_list_attribute"] = [0, 1, 2]
    fh = io.BytesIO()
    with pytest.raises(TypeError, match="GraphML does not support"):
        nx.write_graphml(G, fh)

