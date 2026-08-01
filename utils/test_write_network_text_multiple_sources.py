
def test_write_network_text_multiple_sources():
    g = nx.DiGraph()
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)
    g.add_edge(3, 5)
    g.add_edge(3, 6)
    g.add_edge(5, 4)
    g.add_edge(4, 1)
    g.add_edge(1, 5)
    lines = []
    write = lines.append
    # Use each node as the starting point to demonstrate how the representation
    # changes.
    nodes = sorted(g.nodes())
    for n in nodes:
        write(f"--- source node: {n} ---")
        nx.write_network_text(g, path=write, sources=[n], end="")
    text = "\n".join(lines)
    target = dedent(
        """
        --- source node: 1 ---
        ╙── 1 ╾ 4
            ├─╼ 2
            │   └─╼ 4 ╾ 5
            │       └─╼  ...
            ├─╼ 3
            │   ├─╼ 5 ╾ 1
            │   │   └─╼  ...
            │   └─╼ 6
            └─╼  ...
        --- source node: 2 ---
        ╙── 2 ╾ 1
            └─╼ 4 ╾ 5
                └─╼ 1
                    ├─╼ 3
                    │   ├─╼ 5 ╾ 1
                    │   │   └─╼  ...
                    │   └─╼ 6
                    └─╼  ...
        --- source node: 3 ---
        ╙── 3 ╾ 1
            ├─╼ 5 ╾ 1
            │   └─╼ 4 ╾ 2
            │       └─╼ 1
            │           ├─╼ 2
            │           │   └─╼  ...
            │           └─╼  ...
            └─╼ 6
        --- source node: 4 ---
        ╙── 4 ╾ 2, 5
            └─╼ 1
                ├─╼ 2
                │   └─╼  ...
                ├─╼ 3
                │   ├─╼ 5 ╾ 1
                │   │   └─╼  ...
                │   └─╼ 6
                └─╼  ...
        --- source node: 5 ---
        ╙── 5 ╾ 3, 1
            └─╼ 4 ╾ 2
                └─╼ 1
                    ├─╼ 2
                    │   └─╼  ...
                    ├─╼ 3
                    │   ├─╼ 6
                    │   └─╼  ...
                    └─╼  ...
        --- source node: 6 ---
        ╙── 6 ╾ 3
        """
    ).strip()
    assert target == text

