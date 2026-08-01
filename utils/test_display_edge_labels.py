
def test_display_edge_labels():
    G = nx.path_graph(4)
    canvas = plt.figure().add_subplot(111)
    # While we can pass in dicts for edge label defaults without errors,
    # this isn't helpful unless we want one label for all edges.
    nx.set_edge_attributes(G, {(u, v): {"label": u + v} for u, v in G.edges()})
    nx.display(G, canvas=canvas, edge_label={"color": "r"}, node_label=None)
    labels = [t for t in canvas.get_children() if isinstance(t, mpl.text.Text)]
    print(labels)
    for e, l in zip(G.edges(), labels):
        assert l.get_text() == str(e[0] + e[1])
        assert l.get_color() == "r"
    plt.close()

