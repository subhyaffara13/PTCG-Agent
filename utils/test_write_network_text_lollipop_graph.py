
def test_write_network_text_lollipop_graph():
    graph = nx.lollipop_graph(4, 2, create_using=nx.Graph)
    lines = []
    write = lines.append
    nx.write_network_text(graph, path=write, end="")
    text = "\n".join(lines)
    target = dedent(
        """
        ╙── 5
            └── 4
                └── 3
                    ├── 0
                    │   ├── 1 ─ 3
                    │   │   └── 2 ─ 0, 3
                    │   └──  ...
                    └──  ...
        """
    ).strip()
    assert target == text

