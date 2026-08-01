
def test_write_network_text_path_graph():
    graph = nx.path_graph(3, create_using=nx.Graph)
    lines = []
    write = lines.append
    nx.write_network_text(graph, path=write, end="")
    text = "\n".join(lines)
    target = dedent(
        """
        ╙── 0
            └── 1
                └── 2
        """
    ).strip()
    assert target == text

