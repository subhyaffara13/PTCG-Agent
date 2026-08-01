
def test_termination():
    # ensure termination of asyn_lpa_communities in two cases
    # that led to an endless loop in a previous version
    test1 = nx.karate_club_graph()
    test2 = nx.caveman_graph(2, 10)
    test2.add_edges_from([(0, 20), (20, 10)])
    nx.community.asyn_lpa_communities(test1)
    nx.community.asyn_lpa_communities(test2)

