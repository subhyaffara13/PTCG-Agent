
def test_graph_attributes():
    G = nx.path_graph(4)
    G.add_node(1, color="red")
    G.add_edge(1, 2, width=7)
    G.graph["foo"] = "bar"
    G.graph[1] = "one"
    G.add_node(3, name="node", id="123")

    H = cytoscape_graph(cytoscape_data(G))
    assert H.graph["foo"] == "bar"
    assert H.nodes[1]["color"] == "red"
    assert H[1][2]["width"] == 7
    assert H.nodes[3]["name"] == "node"
    assert H.nodes[3]["id"] == "123"

    d = json.dumps(cytoscape_data(G))
    H = cytoscape_graph(json.loads(d))
    assert H.graph["foo"] == "bar"
    assert H.graph[1] == "one"
    assert H.nodes[1]["color"] == "red"
    assert H[1][2]["width"] == 7
    assert H.nodes[3]["name"] == "node"
    assert H.nodes[3]["id"] == "123"


def test_graph_attributes():
    G = nx.DiGraph()
    G.add_nodes_from([1, 2, 3], color="red")
    G.add_edge(1, 2, foo=7)
    G.add_edge(1, 3, foo=10)
    G.add_edge(3, 4, foo=10)
    H = tree_graph(tree_data(G, 1))
    assert H.nodes[1]["color"] == "red"

    d = json.dumps(tree_data(G, 1))
    H = tree_graph(json.loads(d))
    assert H.nodes[1]["color"] == "red"

