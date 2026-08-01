
def test_generate_network_text_forest_directed():
    # Create a directed forest with labels
    graph = nx.balanced_tree(r=2, h=2, create_using=nx.DiGraph)
    for node in graph.nodes:
        graph.nodes[node]["label"] = "node_" + chr(ord("a") + node)

    node_target = dedent(
        """
        ╙── 0
            ├─╼ 1
            │   ├─╼ 3
            │   └─╼ 4
            └─╼ 2
                ├─╼ 5
                └─╼ 6
        """
    ).strip()

    label_target = dedent(
        """
        ╙── node_a
            ├─╼ node_b
            │   ├─╼ node_d
            │   └─╼ node_e
            └─╼ node_c
                ├─╼ node_f
                └─╼ node_g
        """
    ).strip()

    # Basic node case
    ret = nx.generate_network_text(graph, with_labels=False)
    assert "\n".join(ret) == node_target

    # Basic label case
    ret = nx.generate_network_text(graph, with_labels=True)
    assert "\n".join(ret) == label_target

