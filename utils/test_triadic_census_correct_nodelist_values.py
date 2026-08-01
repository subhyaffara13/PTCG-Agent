
def test_triadic_census_correct_nodelist_values():
    G = nx.path_graph(5, create_using=nx.DiGraph)
    msg = r"nodelist includes duplicate nodes or nodes not in G"
    with pytest.raises(ValueError, match=msg):
        nx.triadic_census(G, [1, 2, 2, 3])
    with pytest.raises(ValueError, match=msg):
        nx.triadic_census(G, [1, 2, "a", 3])

