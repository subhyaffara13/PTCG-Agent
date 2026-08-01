
def test_display_arg_handling_node_alpha(param_value, expected):
    G = nx.path_graph(4)
    nx.set_node_attributes(G, {n: 1 / (n + 1) for n in G.nodes()}, "n_alpha")
    canvas = plt.figure().add_subplot(111)
    nx.display(G, canvas=canvas, node_alpha=param_value)
    assert all(
        canvas.get_children()[0].get_fc()[:, 3] == expected
    )  # Extract just the alpha from the node colors
    plt.close()

