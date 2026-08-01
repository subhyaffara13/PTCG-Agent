
def test_write_network_text_iterative_add_directed_edges():
    """
    Walk through the cases going from a disconnected to fully connected graph
    """
    graph = nx.DiGraph()
    graph.add_nodes_from([1, 2, 3, 4])
    lines = []
    write = lines.append
    write("--- initial state ---")
    nx.write_network_text(graph, path=write, end="")
    for i, j in product(graph.nodes, graph.nodes):
        write(f"--- add_edge({i}, {j}) ---")
        graph.add_edge(i, j)
        nx.write_network_text(graph, path=write, end="")
    text = "\n".join(lines)
    # defined starting point
    target = dedent(
        """
        --- initial state ---
        ╟── 1
        ╟── 2
        ╟── 3
        ╙── 4
        --- add_edge(1, 1) ---
        ╟── 1 ╾ 1
        ╎   └─╼  ...
        ╟── 2
        ╟── 3
        ╙── 4
        --- add_edge(1, 2) ---
        ╟── 1 ╾ 1
        ╎   ├─╼ 2
        ╎   └─╼  ...
        ╟── 3
        ╙── 4
        --- add_edge(1, 3) ---
        ╟── 1 ╾ 1
        ╎   ├─╼ 2
        ╎   ├─╼ 3
        ╎   └─╼  ...
        ╙── 4
        --- add_edge(1, 4) ---
        ╙── 1 ╾ 1
            ├─╼ 2
            ├─╼ 3
            ├─╼ 4
            └─╼  ...
        --- add_edge(2, 1) ---
        ╙── 2 ╾ 1
            └─╼ 1 ╾ 1
                ├─╼ 3
                ├─╼ 4
                └─╼  ...
        --- add_edge(2, 2) ---
        ╙── 1 ╾ 1, 2
            ├─╼ 2 ╾ 2
            │   └─╼  ...
            ├─╼ 3
            ├─╼ 4
            └─╼  ...
        --- add_edge(2, 3) ---
        ╙── 1 ╾ 1, 2
            ├─╼ 2 ╾ 2
            │   ├─╼ 3 ╾ 1
            │   └─╼  ...
            ├─╼ 4
            └─╼  ...
        --- add_edge(2, 4) ---
        ╙── 1 ╾ 1, 2
            ├─╼ 2 ╾ 2
            │   ├─╼ 3 ╾ 1
            │   ├─╼ 4 ╾ 1
            │   └─╼  ...
            └─╼  ...
        --- add_edge(3, 1) ---
        ╙── 2 ╾ 1, 2
            ├─╼ 1 ╾ 1, 3
            │   ├─╼ 3 ╾ 2
            │   │   └─╼  ...
            │   ├─╼ 4 ╾ 2
            │   └─╼  ...
            └─╼  ...
        --- add_edge(3, 2) ---
        ╙── 3 ╾ 1, 2
            ├─╼ 1 ╾ 1, 2
            │   ├─╼ 2 ╾ 2, 3
            │   │   ├─╼ 4 ╾ 1
            │   │   └─╼  ...
            │   └─╼  ...
            └─╼  ...
        --- add_edge(3, 3) ---
        ╙── 1 ╾ 1, 2, 3
            ├─╼ 2 ╾ 2, 3
            │   ├─╼ 3 ╾ 1, 3
            │   │   └─╼  ...
            │   ├─╼ 4 ╾ 1
            │   └─╼  ...
            └─╼  ...
        --- add_edge(3, 4) ---
        ╙── 1 ╾ 1, 2, 3
            ├─╼ 2 ╾ 2, 3
            │   ├─╼ 3 ╾ 1, 3
            │   │   ├─╼ 4 ╾ 1, 2
            │   │   └─╼  ...
            │   └─╼  ...
            └─╼  ...
        --- add_edge(4, 1) ---
        ╙── 2 ╾ 1, 2, 3
            ├─╼ 1 ╾ 1, 3, 4
            │   ├─╼ 3 ╾ 2, 3
            │   │   ├─╼ 4 ╾ 1, 2
            │   │   │   └─╼  ...
            │   │   └─╼  ...
            │   └─╼  ...
            └─╼  ...
        --- add_edge(4, 2) ---
        ╙── 3 ╾ 1, 2, 3
            ├─╼ 1 ╾ 1, 2, 4
            │   ├─╼ 2 ╾ 2, 3, 4
            │   │   ├─╼ 4 ╾ 1, 3
            │   │   │   └─╼  ...
            │   │   └─╼  ...
            │   └─╼  ...
            └─╼  ...
        --- add_edge(4, 3) ---
        ╙── 4 ╾ 1, 2, 3
            ├─╼ 1 ╾ 1, 2, 3
            │   ├─╼ 2 ╾ 2, 3, 4
            │   │   ├─╼ 3 ╾ 1, 3, 4
            │   │   │   └─╼  ...
            │   │   └─╼  ...
            │   └─╼  ...
            └─╼  ...
        --- add_edge(4, 4) ---
        ╙── 1 ╾ 1, 2, 3, 4
            ├─╼ 2 ╾ 2, 3, 4
            │   ├─╼ 3 ╾ 1, 3, 4
            │   │   ├─╼ 4 ╾ 1, 2, 4
            │   │   │   └─╼  ...
            │   │   └─╼  ...
            │   └─╼  ...
            └─╼  ...
        """
    ).strip()
    assert target == text

