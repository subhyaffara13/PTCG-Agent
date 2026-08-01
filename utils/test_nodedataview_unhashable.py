
def test_nodedataview_unhashable():
    G = nx.path_graph(9)
    G.nodes[3]["foo"] = "bar"
    nvs = [G.nodes.data()]
    nvs.append(G.nodes.data(True))
    H = G.copy()
    H.nodes[4]["foo"] = {1, 2, 3}
    nvs.append(H.nodes.data(True))
    # raise unhashable
    for nv in nvs:
        pytest.raises(TypeError, set, nv)
        pytest.raises(TypeError, eval, "nv | nv", locals())
    # no raise... hashable
    Gn = G.nodes.data(False)
    set(Gn)
    Gn | Gn
    Gn = G.nodes.data("foo")
    set(Gn)
    Gn | Gn

