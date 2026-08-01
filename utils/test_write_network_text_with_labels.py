
def test_write_network_text_with_labels():
    graph = nx.generators.complete_graph(5, create_using=nx.DiGraph)
    for n in graph.nodes:
        graph.nodes[n]["label"] = f"Node(n={n})"
    lines = []
    write = lines.append
    nx.write_network_text(graph, path=write, with_labels=True, ascii_only=False, end="")
    text = "\n".join(lines)
    # Non trees with labels can get somewhat out of hand with network text
    # because we need to immediately show every non-tree edge to the right
    target = dedent(
        """
        ╙── Node(n=0) ╾ Node(n=1), Node(n=2), Node(n=3), Node(n=4)
            ├─╼ Node(n=1) ╾ Node(n=2), Node(n=3), Node(n=4)
            │   ├─╼ Node(n=2) ╾ Node(n=0), Node(n=3), Node(n=4)
            │   │   ├─╼ Node(n=3) ╾ Node(n=0), Node(n=1), Node(n=4)
            │   │   │   ├─╼ Node(n=4) ╾ Node(n=0), Node(n=1), Node(n=2)
            │   │   │   │   └─╼  ...
            │   │   │   └─╼  ...
            │   │   └─╼  ...
            │   └─╼  ...
            └─╼  ...
        """
    ).strip()
    assert target == text

