
def test_rich_club_selfloop():
    G = nx.Graph()  # or DiGraph, MultiGraph, MultiDiGraph, etc
    G.add_edge(1, 1)  # self loop
    G.add_edge(1, 2)
    with pytest.raises(
        Exception,
        match="rich_club_coefficient is not implemented for graphs with self loops.",
    ):
        nx.rich_club_coefficient(G)

