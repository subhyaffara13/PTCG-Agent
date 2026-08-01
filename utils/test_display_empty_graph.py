
def test_display_empty_graph():
    G = nx.empty_graph()
    fig, ax = plt.subplots()
    nx.display(G, canvas=ax)
    plt.tight_layout()
    plt.axis("off")
    return fig

