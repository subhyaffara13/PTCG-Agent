
def test_articulation_points():
    Ggen = _generate_no_biconnected()
    for flow_func in flow_funcs:
        for i in range(3):
            G = next(Ggen)
            errmsg = f"Assertion failed in function: {flow_func.__name__}"
            assert nx.node_connectivity(G, flow_func=flow_func) == 1, errmsg


def test_articulation_points():
    Ggen = _generate_no_biconnected()
    for flow_func in flow_funcs:
        errmsg = f"Assertion failed in function: {flow_func.__name__}"
        for i in range(1):  # change 1 to 3 or more for more realizations.
            G = next(Ggen)
            cut = nx.minimum_node_cut(G, flow_func=flow_func)
            assert len(cut) == 1, errmsg
            assert cut.pop() in set(nx.articulation_points(G)), errmsg


def test_articulation_points():
    Ggen = _generate_no_biconnected()
    for i in range(1):  # change 1 to 3 or more for more realizations.
        G = next(Ggen)
        articulation_points = [{a} for a in nx.articulation_points(G)]
        for cut in nx.all_node_cuts(G):
            assert cut in articulation_points

