
def test_write_network_text_nearly_forest():
    g = nx.DiGraph()
    g.add_edge(1, 2)
    g.add_edge(1, 5)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(5, 6)
    g.add_edge(6, 7)
    g.add_edge(6, 8)
    orig = g.copy()
    g.add_edge(1, 8)  # forward edge
    g.add_edge(4, 2)  # back edge
    g.add_edge(6, 3)  # cross edge
    lines = []
    write = lines.append
    write("--- directed case ---")
    nx.write_network_text(orig, path=write, end="")
    write("--- add (1, 8), (4, 2), (6, 3) ---")
    nx.write_network_text(g, path=write, end="")
    write("--- undirected case ---")
    nx.write_network_text(orig.to_undirected(), path=write, sources=[1], end="")
    write("--- add (1, 8), (4, 2), (6, 3) ---")
    nx.write_network_text(g.to_undirected(), path=write, sources=[1], end="")
    text = "\n".join(lines)
    target = dedent(
        """
        --- directed case ---
        ╙── 1
            ├─╼ 2
            │   └─╼ 3
            │       └─╼ 4
            └─╼ 5
                └─╼ 6
                    ├─╼ 7
                    └─╼ 8
        --- add (1, 8), (4, 2), (6, 3) ---
        ╙── 1
            ├─╼ 2 ╾ 4
            │   └─╼ 3 ╾ 6
            │       └─╼ 4
            │           └─╼  ...
            ├─╼ 5
            │   └─╼ 6
            │       ├─╼ 7
            │       ├─╼ 8 ╾ 1
            │       └─╼  ...
            └─╼  ...
        --- undirected case ---
        ╙── 1
            ├── 2
            │   └── 3
            │       └── 4
            └── 5
                └── 6
                    ├── 7
                    └── 8
        --- add (1, 8), (4, 2), (6, 3) ---
        ╙── 1
            ├── 2
            │   ├── 3
            │   │   ├── 4 ─ 2
            │   │   └── 6
            │   │       ├── 5 ─ 1
            │   │       ├── 7
            │   │       └── 8 ─ 1
            │   └──  ...
            └──  ...
        """
    ).strip()
    assert target == text

