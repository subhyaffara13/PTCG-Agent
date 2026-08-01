
def test_write_network_text_circular_ladder_graph():
    graph = nx.circular_ladder_graph(4, create_using=nx.Graph)
    lines = []
    write = lines.append
    nx.write_network_text(graph, path=write, end="")
    text = "\n".join(lines)
    target = dedent(
        """
        ╙── 0
            ├── 1
            │   ├── 2
            │   │   ├── 3 ─ 0
            │   │   │   └── 7
            │   │   │       ├── 6 ─ 2
            │   │   │       │   └── 5 ─ 1
            │   │   │       │       └── 4 ─ 0, 7
            │   │   │       └──  ...
            │   │   └──  ...
            │   └──  ...
            └──  ...
        """
    ).strip()
    assert target == text

