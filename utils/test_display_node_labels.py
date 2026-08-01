
def test_display_node_labels():
    G = nx.path_graph(4)
    canvas = plt.figure().add_subplot(111)
    nx.display(G, canvas=canvas, node_label={"size": 20})
    labels = [t for t in canvas.get_children() if isinstance(t, mpl.text.Text)]
    for n, l in zip(G.nodes(), labels):
        assert l.get_text() == str(n)
        assert l.get_size() == 20.0
    plt.close()

