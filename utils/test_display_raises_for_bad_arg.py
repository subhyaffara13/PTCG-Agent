
def test_display_raises_for_bad_arg():
    G = nx.karate_club_graph()
    with pytest.raises(nx.NetworkXError):
        nx.display(G, bad_arg="bad_arg")
        plt.close()

