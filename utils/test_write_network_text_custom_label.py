
def test_write_network_text_custom_label():
    # Create a directed forest with labels
    graph = nx.erdos_renyi_graph(5, 0.4, directed=True, seed=359222358)
    for node in graph.nodes:
        graph.nodes[node]["label"] = f"Node({node})"
        graph.nodes[node]["chr"] = chr(node + ord("a") - 1)
        if node % 2 == 0:
            graph.nodes[node]["part"] = chr(node + ord("a"))

    lines = []
    write = lines.append
    write("--- when with_labels=True, uses the 'label' attr ---")
    nx.write_network_text(graph, path=write, with_labels=True, end="", max_depth=None)
    write("--- when with_labels=False, uses str(node) value ---")
    nx.write_network_text(graph, path=write, with_labels=False, end="", max_depth=None)
    write("--- when with_labels is a string, use that attr ---")
    nx.write_network_text(graph, path=write, with_labels="chr", end="", max_depth=None)
    write("--- fallback to str(node) when the attr does not exist ---")
    nx.write_network_text(graph, path=write, with_labels="part", end="", max_depth=None)

    text = "\n".join(lines)
    target = dedent(
        """
        --- when with_labels=True, uses the 'label' attr ---
        ╙── Node(1)
            └─╼ Node(3) ╾ Node(2)
                ├─╼ Node(0)
                │   ├─╼ Node(2) ╾ Node(3), Node(4)
                │   │   └─╼  ...
                │   └─╼ Node(4)
                │       └─╼  ...
                └─╼  ...
        --- when with_labels=False, uses str(node) value ---
        ╙── 1
            └─╼ 3 ╾ 2
                ├─╼ 0
                │   ├─╼ 2 ╾ 3, 4
                │   │   └─╼  ...
                │   └─╼ 4
                │       └─╼  ...
                └─╼  ...
        --- when with_labels is a string, use that attr ---
        ╙── a
            └─╼ c ╾ b
                ├─╼ `
                │   ├─╼ b ╾ c, d
                │   │   └─╼  ...
                │   └─╼ d
                │       └─╼  ...
                └─╼  ...
        --- fallback to str(node) when the attr does not exist ---
        ╙── 1
            └─╼ 3 ╾ c
                ├─╼ a
                │   ├─╼ c ╾ 3, e
                │   │   └─╼  ...
                │   └─╼ e
                │       └─╼  ...
                └─╼  ...
        """
    ).strip()
    assert target == text

