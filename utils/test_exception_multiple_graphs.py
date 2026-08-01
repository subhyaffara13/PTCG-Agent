
def test_exception_multiple_graphs(to_latex=nx.to_latex):
    G = nx.path_graph(3)
    pos_bad = {0: (1, 2), 1: (0, 1)}
    pos_OK = {0: (1, 2), 1: (0, 1), 2: (2, 1)}
    fourG = [G, G, G, G]
    fourpos = [pos_OK, pos_OK, pos_OK, pos_OK]

    # input single dict to use for all graphs
    to_latex(fourG, pos_OK)
    with pytest.raises(nx.NetworkXError):
        to_latex(fourG, pos_bad)

    # input list of dicts to use for all graphs
    to_latex(fourG, fourpos)
    with pytest.raises(nx.NetworkXError):
        to_latex(fourG, [pos_bad, pos_bad, pos_bad, pos_bad])

    # every pos dict must include all nodes
    with pytest.raises(nx.NetworkXError):
        to_latex(fourG, [pos_OK, pos_OK, pos_bad, pos_OK])

    # test sub_captions and sub_labels (len must match Gbunch)
    with pytest.raises(nx.NetworkXError):
        to_latex(fourG, fourpos, sub_captions=["hi", "hi"])

    with pytest.raises(nx.NetworkXError):
        to_latex(fourG, fourpos, sub_labels=["hi", "hi"])

    # all pass
    to_latex(fourG, fourpos, sub_captions=["hi"] * 4, sub_labels=["lbl"] * 4)

