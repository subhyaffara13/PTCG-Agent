
def test_generate_network_text_overspecified_sources():
    """
    When sources are directly specified, we won't be able to determine when we
    are in the last component, so there will always be a trailing, leftmost
    pipe.
    """
    graph = nx.disjoint_union_all(
        [
            nx.balanced_tree(r=2, h=1, create_using=nx.DiGraph),
            nx.balanced_tree(r=1, h=2, create_using=nx.DiGraph),
            nx.balanced_tree(r=2, h=1, create_using=nx.DiGraph),
        ]
    )

    # defined starting point
    target1 = dedent(
        """
        ╟── 0
        ╎   ├─╼ 1
        ╎   └─╼ 2
        ╟── 3
        ╎   └─╼ 4
        ╎       └─╼ 5
        ╟── 6
        ╎   ├─╼ 7
        ╎   └─╼ 8
        """
    ).strip()

    target2 = dedent(
        """
        ╟── 0
        ╎   ├─╼ 1
        ╎   └─╼ 2
        ╟── 3
        ╎   └─╼ 4
        ╎       └─╼ 5
        ╙── 6
            ├─╼ 7
            └─╼ 8
        """
    ).strip()

    got1 = "\n".join(nx.generate_network_text(graph, sources=graph.nodes))
    got2 = "\n".join(nx.generate_network_text(graph))
    assert got1 == target1
    assert got2 == target2

