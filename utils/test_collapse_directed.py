
def test_collapse_directed():
    graph = nx.balanced_tree(r=2, h=3, create_using=nx.DiGraph)
    lines = []
    write = lines.append
    write("--- Original ---")
    nx.write_network_text(graph, path=write, end="")
    graph.nodes[1]["collapse"] = True
    write("--- Collapse Node 1 ---")
    nx.write_network_text(graph, path=write, end="")
    write("--- Add alternate path (5, 3) to collapsed zone")
    graph.add_edge(5, 3)
    nx.write_network_text(graph, path=write, end="")
    write("--- Collapse Node 0 ---")
    graph.nodes[0]["collapse"] = True
    nx.write_network_text(graph, path=write, end="")
    text = "\n".join(lines)
    target = dedent(
        """
        --- Original ---
        ╙── 0
            ├─╼ 1
            │   ├─╼ 3
            │   │   ├─╼ 7
            │   │   └─╼ 8
            │   └─╼ 4
            │       ├─╼ 9
            │       └─╼ 10
            └─╼ 2
                ├─╼ 5
                │   ├─╼ 11
                │   └─╼ 12
                └─╼ 6
                    ├─╼ 13
                    └─╼ 14
        --- Collapse Node 1 ---
        ╙── 0
            ├─╼ 1
            │   └─╼  ...
            └─╼ 2
                ├─╼ 5
                │   ├─╼ 11
                │   └─╼ 12
                └─╼ 6
                    ├─╼ 13
                    └─╼ 14
        --- Add alternate path (5, 3) to collapsed zone
        ╙── 0
            ├─╼ 1
            │   └─╼  ...
            └─╼ 2
                ├─╼ 5
                │   ├─╼ 11
                │   ├─╼ 12
                │   └─╼ 3 ╾ 1
                │       ├─╼ 7
                │       └─╼ 8
                └─╼ 6
                    ├─╼ 13
                    └─╼ 14
        --- Collapse Node 0 ---
        ╙── 0
            └─╼  ...
        """
    ).strip()
    assert target == text

