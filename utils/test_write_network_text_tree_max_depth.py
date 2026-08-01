
def test_write_network_text_tree_max_depth():
    orig = nx.balanced_tree(r=1, h=3, create_using=nx.DiGraph)
    lines = []
    write = lines.append
    write("--- directed case, max_depth=0 ---")
    nx.write_network_text(orig, path=write, end="", max_depth=0)
    write("--- directed case, max_depth=1 ---")
    nx.write_network_text(orig, path=write, end="", max_depth=1)
    write("--- directed case, max_depth=2 ---")
    nx.write_network_text(orig, path=write, end="", max_depth=2)
    write("--- directed case, max_depth=3 ---")
    nx.write_network_text(orig, path=write, end="", max_depth=3)
    write("--- directed case, max_depth=4 ---")
    nx.write_network_text(orig, path=write, end="", max_depth=4)
    write("--- undirected case, max_depth=0 ---")
    nx.write_network_text(orig.to_undirected(), path=write, end="", max_depth=0)
    write("--- undirected case, max_depth=1 ---")
    nx.write_network_text(orig.to_undirected(), path=write, end="", max_depth=1)
    write("--- undirected case, max_depth=2 ---")
    nx.write_network_text(orig.to_undirected(), path=write, end="", max_depth=2)
    write("--- undirected case, max_depth=3 ---")
    nx.write_network_text(orig.to_undirected(), path=write, end="", max_depth=3)
    write("--- undirected case, max_depth=4 ---")
    nx.write_network_text(orig.to_undirected(), path=write, end="", max_depth=4)
    text = "\n".join(lines)
    target = dedent(
        """
        --- directed case, max_depth=0 ---
        ╙ ...
        --- directed case, max_depth=1 ---
        ╙── 0
            └─╼  ...
        --- directed case, max_depth=2 ---
        ╙── 0
            └─╼ 1
                └─╼  ...
        --- directed case, max_depth=3 ---
        ╙── 0
            └─╼ 1
                └─╼ 2
                    └─╼  ...
        --- directed case, max_depth=4 ---
        ╙── 0
            └─╼ 1
                └─╼ 2
                    └─╼ 3
        --- undirected case, max_depth=0 ---
        ╙ ...
        --- undirected case, max_depth=1 ---
        ╙── 0 ─ 1
            └──  ...
        --- undirected case, max_depth=2 ---
        ╙── 0
            └── 1 ─ 2
                └──  ...
        --- undirected case, max_depth=3 ---
        ╙── 0
            └── 1
                └── 2 ─ 3
                    └──  ...
        --- undirected case, max_depth=4 ---
        ╙── 0
            └── 1
                └── 2
                    └── 3
        """
    ).strip()
    assert target == text

