
def test_write_network_text_clique_max_depth():
    orig = nx.complete_graph(5, nx.DiGraph)
    lines = []
    write = lines.append
    write("--- directed case, max_depth=None ---")
    nx.write_network_text(orig, path=write, end="", max_depth=None)
    write("--- directed case, max_depth=0 ---")
    nx.write_network_text(orig, path=write, end="", max_depth=0)
    write("--- directed case, max_depth=1 ---")
    nx.write_network_text(orig, path=write, end="", max_depth=1)
    write("--- directed case, max_depth=2 ---")
    nx.write_network_text(orig, path=write, end="", max_depth=2)
    write("--- directed case, max_depth=3 ---")
    nx.write_network_text(orig, path=write, end="", max_depth=3)
    write("--- undirected case, max_depth=None ---")
    nx.write_network_text(orig.to_undirected(), path=write, end="", max_depth=None)
    write("--- undirected case, max_depth=0 ---")
    nx.write_network_text(orig.to_undirected(), path=write, end="", max_depth=0)
    write("--- undirected case, max_depth=1 ---")
    nx.write_network_text(orig.to_undirected(), path=write, end="", max_depth=1)
    write("--- undirected case, max_depth=2 ---")
    nx.write_network_text(orig.to_undirected(), path=write, end="", max_depth=2)
    write("--- undirected case, max_depth=3 ---")
    nx.write_network_text(orig.to_undirected(), path=write, end="", max_depth=3)
    text = "\n".join(lines)
    target = dedent(
        """
        --- directed case, max_depth=None ---
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
        --- directed case, max_depth=0 ---
        ╙ ...
        --- directed case, max_depth=1 ---
        ╙── 0 ╾ 1, 2, 3, 4
            └─╼  ...
        --- directed case, max_depth=2 ---
        ╙── 0 ╾ 1, 2, 3, 4
            ├─╼ 1 ╾ 2, 3, 4
            │   └─╼  ...
            ├─╼ 2 ╾ 1, 3, 4
            │   └─╼  ...
            ├─╼ 3 ╾ 1, 2, 4
            │   └─╼  ...
            └─╼ 4 ╾ 1, 2, 3
                └─╼  ...
        --- directed case, max_depth=3 ---
        ╙── 0 ╾ 1, 2, 3, 4
            ├─╼ 1 ╾ 2, 3, 4
            │   ├─╼ 2 ╾ 0, 3, 4
            │   │   └─╼  ...
            │   ├─╼ 3 ╾ 0, 2, 4
            │   │   └─╼  ...
            │   ├─╼ 4 ╾ 0, 2, 3
            │   │   └─╼  ...
            │   └─╼  ...
            └─╼  ...
        --- undirected case, max_depth=None ---
        ╙── 0
            ├── 1
            │   ├── 2 ─ 0
            │   │   ├── 3 ─ 0, 1
            │   │   │   └── 4 ─ 0, 1, 2
            │   │   └──  ...
            │   └──  ...
            └──  ...
        --- undirected case, max_depth=0 ---
        ╙ ...
        --- undirected case, max_depth=1 ---
        ╙── 0 ─ 1, 2, 3, 4
            └──  ...
        --- undirected case, max_depth=2 ---
        ╙── 0
            ├── 1 ─ 2, 3, 4
            │   └──  ...
            ├── 2 ─ 1, 3, 4
            │   └──  ...
            ├── 3 ─ 1, 2, 4
            │   └──  ...
            └── 4 ─ 1, 2, 3
        --- undirected case, max_depth=3 ---
        ╙── 0
            ├── 1
            │   ├── 2 ─ 0, 3, 4
            │   │   └──  ...
            │   ├── 3 ─ 0, 2, 4
            │   │   └──  ...
            │   └── 4 ─ 0, 2, 3
            └──  ...
        """
    ).strip()
    assert target == text

