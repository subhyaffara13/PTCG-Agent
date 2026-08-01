
def test_individualized_font_attributes(subplots):
    G = nx.karate_club_graph()
    fig, ax = subplots
    nx.draw(
        G,
        ax=ax,
        font_color={n: "k" if n % 2 else "r" for n in G.nodes()},
        font_size={n: int(n / (34 / 15) + 5) for n in G.nodes()},
    )
    for n, t in zip(
        G.nodes(),
        [
            t
            for t in ax.get_children()
            if isinstance(t, mpl.text.Text) and len(t.get_text()) > 0
        ],
    ):
        expected = "black" if n % 2 else "red"

        assert mpl.colors.same_color(t.get_color(), expected)
        assert int(n / (34 / 15) + 5) == t.get_size()

