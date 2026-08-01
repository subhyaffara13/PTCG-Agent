
def test_write_network_text_wheel_graph():
    graph = nx.wheel_graph(7, create_using=nx.Graph)
    lines = []
    write = lines.append
    nx.write_network_text(graph, path=write, end="")
    text = "\n".join(lines)
    target = dedent(
        """
        ╙── 1
            ├── 0
            │   ├── 2 ─ 1
            │   │   └── 3 ─ 0
            │   │       └── 4 ─ 0
            │   │           └── 5 ─ 0
            │   │               └── 6 ─ 0, 1
            │   └──  ...
            └──  ...
        """
    ).strip()
    assert target == text

