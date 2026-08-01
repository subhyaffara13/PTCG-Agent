
def test_factories():
    class mydict1(dict):
        pass

    class mydict2(dict):
        pass

    class mydict3(dict):
        pass

    class mydict4(dict):
        pass

    class mydict5(dict):
        pass

    for Graph in (nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph):

        class MyGraph(Graph):
            node_dict_factory = mydict1
            adjlist_outer_dict_factory = mydict2
            adjlist_inner_dict_factory = mydict3
            edge_key_dict_factory = mydict4
            edge_attr_dict_factory = mydict5

        G = MyGraph()
        assert isinstance(G._node, mydict1)
        assert isinstance(G._adj, mydict2)
        G.add_node(1)
        assert isinstance(G._adj[1], mydict3)
        if G.is_directed():
            assert isinstance(G._pred, mydict2)
            assert isinstance(G._succ, mydict2)
            assert isinstance(G._pred[1], mydict3)
        G.add_edge(1, 2)
        if G.is_multigraph():
            assert isinstance(G._adj[1][2], mydict4)
            assert isinstance(G._adj[1][2][0], mydict5)
        else:
            assert isinstance(G._adj[1][2], mydict5)

