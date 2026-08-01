
def test_display_node_position():
    G = nx.path_graph(4)
    nx.set_node_attributes(G, {n: (n, n) for n in G.nodes()}, "pos")
    canvas = plt.figure().add_subplot(111)
    nx.display(G, canvas=canvas, node_pos="pos")
    assert np.all(
        canvas.get_children()[0].get_offsets().data == [[0, 0], [1, 1], [2, 2], [3, 3]]
    )
    plt.close()

