
def test_display_self_loop():
    ax = plt.axes()
    G = nx.DiGraph()
    G.add_node(0)
    G.add_edge(0, 0)
    nx.set_node_attributes(G, {0: (0, 0)}, "pos")
    nx.display(G, canvas=ax)
    arrow = [
        f for f in ax.get_children() if isinstance(f, mpl.patches.FancyArrowPatch)
    ][0]
    bbox = arrow.get_extents()
    print(bbox.width)
    print(bbox.height)
    assert bbox.width > 0 and bbox.height > 0

    plt.delaxes(ax)
    plt.close()

