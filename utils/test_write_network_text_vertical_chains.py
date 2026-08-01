
def test_write_network_text_vertical_chains():
    graph1 = nx.lollipop_graph(4, 2, create_using=nx.Graph)
    graph1.add_edge(0, -1)
    graph1.add_edge(-1, -2)
    graph1.add_edge(-2, -3)

    graph2 = graph1.to_directed()
    graph2.remove_edges_from([(u, v) for u, v in graph2.edges if v > u])

    lines = []
    write = lines.append
    write("--- Undirected UTF ---")
    nx.write_network_text(graph1, path=write, end="", vertical_chains=True)
    write("--- Undirected ASCI ---")
    nx.write_network_text(
        graph1, path=write, end="", vertical_chains=True, ascii_only=True
    )
    write("--- Directed UTF ---")
    nx.write_network_text(graph2, path=write, end="", vertical_chains=True)
    write("--- Directed ASCI ---")
    nx.write_network_text(
        graph2, path=write, end="", vertical_chains=True, ascii_only=True
    )

    text = "\n".join(lines)
    target = dedent(
        """
        --- Undirected UTF ---
        ╙── 5
            │
            4
            │
            3
            ├── 0
            │   ├── 1 ─ 3
            │   │   │
            │   │   2 ─ 0, 3
            │   ├── -1
            │   │   │
            │   │   -2
            │   │   │
            │   │   -3
            │   └──  ...
            └──  ...
        --- Undirected ASCI ---
        +-- 5
            |
            4
            |
            3
            |-- 0
            |   |-- 1 - 3
            |   |   |
            |   |   2 - 0, 3
            |   |-- -1
            |   |   |
            |   |   -2
            |   |   |
            |   |   -3
            |   L--  ...
            L--  ...
        --- Directed UTF ---
        ╙── 5
            ╽
            4
            ╽
            3
            ├─╼ 0 ╾ 1, 2
            │   ╽
            │   -1
            │   ╽
            │   -2
            │   ╽
            │   -3
            ├─╼ 1 ╾ 2
            │   └─╼  ...
            └─╼ 2
                └─╼  ...
        --- Directed ASCI ---
        +-- 5
            !
            4
            !
            3
            |-> 0 <- 1, 2
            |   !
            |   -1
            |   !
            |   -2
            |   !
            |   -3
            |-> 1 <- 2
            |   L->  ...
            L-> 2
                L->  ...
        """
    ).strip()
    assert target == text

