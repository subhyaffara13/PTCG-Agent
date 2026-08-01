
def test_write_network_text_complete_graphs():
    lines = []
    write = lines.append
    for k in [0, 1, 2, 3, 4, 5]:
        g = nx.generators.complete_graph(k)
        write(f"--- undirected k={k} ---")
        nx.write_network_text(g, path=write, end="")

    for k in [0, 1, 2, 3, 4, 5]:
        g = nx.generators.complete_graph(k, nx.DiGraph)
        write(f"--- directed k={k} ---")
        nx.write_network_text(g, path=write, end="")
    text = "\n".join(lines)
    target = dedent(
        """
        --- undirected k=0 ---
        ╙
        --- undirected k=1 ---
        ╙── 0
        --- undirected k=2 ---
        ╙── 0
            └── 1
        --- undirected k=3 ---
        ╙── 0
            ├── 1
            │   └── 2 ─ 0
            └──  ...
        --- undirected k=4 ---
        ╙── 0
            ├── 1
            │   ├── 2 ─ 0
            │   │   └── 3 ─ 0, 1
            │   └──  ...
            └──  ...
        --- undirected k=5 ---
        ╙── 0
            ├── 1
            │   ├── 2 ─ 0
            │   │   ├── 3 ─ 0, 1
            │   │   │   └── 4 ─ 0, 1, 2
            │   │   └──  ...
            │   └──  ...
            └──  ...
        --- directed k=0 ---
        ╙
        --- directed k=1 ---
        ╙── 0
        --- directed k=2 ---
        ╙── 0 ╾ 1
            └─╼ 1
                └─╼  ...
        --- directed k=3 ---
        ╙── 0 ╾ 1, 2
            ├─╼ 1 ╾ 2
            │   ├─╼ 2 ╾ 0
            │   │   └─╼  ...
            │   └─╼  ...
            └─╼  ...
        --- directed k=4 ---
        ╙── 0 ╾ 1, 2, 3
            ├─╼ 1 ╾ 2, 3
            │   ├─╼ 2 ╾ 0, 3
            │   │   ├─╼ 3 ╾ 0, 1
            │   │   │   └─╼  ...
            │   │   └─╼  ...
            │   └─╼  ...
            └─╼  ...
        --- directed k=5 ---
        ╙── 0 ╾ 1, 2, 3, 4
            ├─╼ 1 ╾ 2, 3, 4
            │   ├─╼ 2 ╾ 0, 3, 4
            │   │   ├─╼ 3 ╾ 0, 1, 4
            │   │   │   ├─╼ 4 ╾ 0, 1, 2
            │   │   │   │   └─╼  ...
            │   │   │   └─╼  ...
            │   │   └─╼  ...
            │   └─╼  ...
            └─╼  ...
        """
    ).strip()
    assert target == text

