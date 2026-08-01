
def test_display_position_function():
    G = nx.karate_club_graph()

    def fixed_layout(G):
        return nx.spring_layout(G, seed=314159)

    pos = fixed_layout(G)
    ax = plt.figure().add_subplot(111)
    nx.display(G, node_pos=fixed_layout, canvas=ax)
    # rebuild the position dictionary from the canvas
    act_pos = {
        n: tuple(p) for n, p in zip(G.nodes(), ax.get_children()[0].get_offsets().data)
    }
    for n in G.nodes():
        assert all(pos[n] == act_pos[n])
    plt.close()

