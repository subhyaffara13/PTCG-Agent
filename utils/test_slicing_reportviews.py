
def test_slicing_reportviews(reportview, err_msg_terms):
    G = nx.complete_graph(3)
    view = reportview(G)
    with pytest.raises(nx.NetworkXError) as exc:
        view[0:2]
    errmsg = str(exc.value)
    assert type(view).__name__ in errmsg
    assert err_msg_terms in errmsg

