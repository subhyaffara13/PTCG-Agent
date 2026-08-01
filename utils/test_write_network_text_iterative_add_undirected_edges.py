
def test_write_network_text_iterative_add_undirected_edges():
    """
    Walk through the cases going from a disconnected to fully connected graph
    """
    graph = nx.Graph()
    graph.add_nodes_from([1, 2, 3, 4])
    lines = []
    write = lines.append
    write("--- initial state ---")
    nx.write_network_text(graph, path=write, end="")
    for i, j in product(graph.nodes, graph.nodes):
        if i == j:
            continue
        write(f"--- add_edge({i}, {j}) ---")
        graph.add_edge(i, j)
        nx.write_network_text(graph, path=write, end="")
    text = "\n".join(lines)
    target = dedent(
        """
        --- initial state ---
        ╟── 1
        ╟── 2
        ╟── 3
        ╙── 4
        --- add_edge(1, 2) ---
        ╟── 3
        ╟── 4
        ╙── 1
            └── 2
        --- add_edge(1, 3) ---
        ╟── 4
        ╙── 2
            └── 1
                └── 3
        --- add_edge(1, 4) ---
        ╙── 2
            └── 1
                ├── 3
                └── 4
        --- add_edge(2, 1) ---
        ╙── 2
            └── 1
                ├── 3
                └── 4
        --- add_edge(2, 3) ---
        ╙── 4
            └── 1
                ├── 2
                │   └── 3 ─ 1
                └──  ...
        --- add_edge(2, 4) ---
        ╙── 3
            ├── 1
            │   ├── 2 ─ 3
            │   │   └── 4 ─ 1
            │   └──  ...
            └──  ...
        --- add_edge(3, 1) ---
        ╙── 3
            ├── 1
            │   ├── 2 ─ 3
            │   │   └── 4 ─ 1
            │   └──  ...
            └──  ...
        --- add_edge(3, 2) ---
        ╙── 3
            ├── 1
            │   ├── 2 ─ 3
            │   │   └── 4 ─ 1
            │   └──  ...
            └──  ...
        --- add_edge(3, 4) ---
        ╙── 1
            ├── 2
            │   ├── 3 ─ 1
            │   │   └── 4 ─ 1, 2
            │   └──  ...
            └──  ...
        --- add_edge(4, 1) ---
        ╙── 1
            ├── 2
            │   ├── 3 ─ 1
            │   │   └── 4 ─ 1, 2
            │   └──  ...
            └──  ...
        --- add_edge(4, 2) ---
        ╙── 1
            ├── 2
            │   ├── 3 ─ 1
            │   │   └── 4 ─ 1, 2
            │   └──  ...
            └──  ...
        --- add_edge(4, 3) ---
        ╙── 1
            ├── 2
            │   ├── 3 ─ 1
            │   │   └── 4 ─ 1, 2
            │   └──  ...
            └──  ...
        """
    ).strip()
    assert target == text

