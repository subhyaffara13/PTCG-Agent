
def test_write_network_text_complete_graph_ascii_only():
    graph = nx.generators.complete_graph(5, create_using=nx.DiGraph)
    lines = []
    write = lines.append
    write("--- directed case ---")
    nx.write_network_text(graph, path=write, ascii_only=True, end="")
    write("--- undirected case ---")
    nx.write_network_text(graph.to_undirected(), path=write, ascii_only=True, end="")
    text = "\n".join(lines)
    target = dedent(
        """
        --- directed case ---
        +-- 0 <- 1, 2, 3, 4
            |-> 1 <- 2, 3, 4
            |   |-> 2 <- 0, 3, 4
            |   |   |-> 3 <- 0, 1, 4
            |   |   |   |-> 4 <- 0, 1, 2
            |   |   |   |   L->  ...
            |   |   |   L->  ...
            |   |   L->  ...
            |   L->  ...
            L->  ...
        --- undirected case ---
        +-- 0
            |-- 1
            |   |-- 2 - 0
            |   |   |-- 3 - 0, 1
            |   |   |   L-- 4 - 0, 1, 2
            |   |   L--  ...
            |   L--  ...
            L--  ...
        """
    ).strip()
    assert target == text

