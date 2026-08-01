
def test_read_edgelist_with_data(data, extra_kwargs, expected):
    bytesIO = io.BytesIO(data.encode("utf-8"))
    G = nx.read_edgelist(bytesIO, nodetype=int, **extra_kwargs)
    assert edges_equal(G.edges(data=True), expected)

