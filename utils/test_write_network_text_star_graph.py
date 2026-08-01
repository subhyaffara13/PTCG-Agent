
def test_write_network_text_star_graph():
    graph = nx.star_graph(5, create_using=nx.Graph)
    lines = []
    write = lines.append
    nx.write_network_text(graph, path=write, end="")
    text = "\n".join(lines)
    target = dedent(
        """
        ╙── 1
            └── 0
                ├── 2
                ├── 3
                ├── 4
                └── 5
        """
    ).strip()
    assert target == text

