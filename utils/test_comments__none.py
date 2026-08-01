
def test_comments_None():
    edgelist = ["node#1 node#2", "node#2 node#3"]
    # comments=None supported to ignore all comment characters
    G = nx.parse_edgelist(edgelist, comments=None)
    H = nx.Graph([e.split(" ") for e in edgelist])
    assert edges_equal(G.edges, H.edges)

