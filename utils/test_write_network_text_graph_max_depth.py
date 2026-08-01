
def test_write_network_text_graph_max_depth():
    orig = nx.erdos_renyi_graph(10, 0.15, directed=True, seed=40392)
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
        ╟── 4
        ╎   ├─╼ 0 ╾ 3
        ╎   ├─╼ 5 ╾ 7
        ╎   │   └─╼ 3
        ╎   │       ├─╼ 1 ╾ 9
        ╎   │       │   └─╼ 9 ╾ 6
        ╎   │       │       ├─╼ 6
        ╎   │       │       │   └─╼  ...
        ╎   │       │       ├─╼ 7 ╾ 4
        ╎   │       │       │   ├─╼ 2
        ╎   │       │       │   └─╼  ...
        ╎   │       │       └─╼  ...
        ╎   │       └─╼  ...
        ╎   └─╼  ...
        ╙── 8
        --- directed case, max_depth=0 ---
        ╙ ...
        --- directed case, max_depth=1 ---
        ╟── 4
        ╎   └─╼  ...
        ╙── 8
        --- directed case, max_depth=2 ---
        ╟── 4
        ╎   ├─╼ 0 ╾ 3
        ╎   ├─╼ 5 ╾ 7
        ╎   │   └─╼  ...
        ╎   └─╼ 7 ╾ 9
        ╎       └─╼  ...
        ╙── 8
        --- directed case, max_depth=3 ---
        ╟── 4
        ╎   ├─╼ 0 ╾ 3
        ╎   ├─╼ 5 ╾ 7
        ╎   │   └─╼ 3
        ╎   │       └─╼  ...
        ╎   └─╼ 7 ╾ 9
        ╎       ├─╼ 2
        ╎       └─╼  ...
        ╙── 8
        --- undirected case, max_depth=None ---
        ╟── 8
        ╙── 2
            └── 7
                ├── 4
                │   ├── 0
                │   │   └── 3
                │   │       ├── 1
                │   │       │   └── 9 ─ 7
                │   │       │       └── 6
                │   │       └── 5 ─ 4, 7
                │   └──  ...
                └──  ...
        --- undirected case, max_depth=0 ---
        ╙ ...
        --- undirected case, max_depth=1 ---
        ╟── 8
        ╙── 2 ─ 7
            └──  ...
        --- undirected case, max_depth=2 ---
        ╟── 8
        ╙── 2
            └── 7 ─ 4, 5, 9
                └──  ...
        --- undirected case, max_depth=3 ---
        ╟── 8
        ╙── 2
            └── 7
                ├── 4 ─ 0, 5
                │   └──  ...
                ├── 5 ─ 4, 3
                │   └──  ...
                └── 9 ─ 1, 6
                    └──  ...
        """
    ).strip()
    assert target == text

