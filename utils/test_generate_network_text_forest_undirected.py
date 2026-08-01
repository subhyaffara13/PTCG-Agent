
def test_generate_network_text_forest_undirected():
    # Create a directed forest
    graph = nx.balanced_tree(r=2, h=2, create_using=nx.Graph)

    node_target0 = dedent(
        """
        ╙── 0
            ├── 1
            │   ├── 3
            │   └── 4
            └── 2
                ├── 5
                └── 6
        """
    ).strip()

    # defined starting point
    ret = "\n".join(nx.generate_network_text(graph, sources=[0]))
    assert ret == node_target0

    # defined starting point
    node_target2 = dedent(
        """
        ╙── 2
            ├── 0
            │   └── 1
            │       ├── 3
            │       └── 4
            ├── 5
            └── 6
        """
    ).strip()
    ret = "\n".join(nx.generate_network_text(graph, sources=[2]))
    assert ret == node_target2

