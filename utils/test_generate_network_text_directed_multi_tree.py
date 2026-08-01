
def test_generate_network_text_directed_multi_tree():
    tree1 = nx.balanced_tree(r=2, h=2, create_using=nx.DiGraph)
    tree2 = nx.balanced_tree(r=2, h=2, create_using=nx.DiGraph)
    forest = nx.disjoint_union_all([tree1, tree2])
    ret = "\n".join(nx.generate_network_text(forest))

    target = dedent(
        """
        ╟── 0
        ╎   ├─╼ 1
        ╎   │   ├─╼ 3
        ╎   │   └─╼ 4
        ╎   └─╼ 2
        ╎       ├─╼ 5
        ╎       └─╼ 6
        ╙── 7
            ├─╼ 8
            │   ├─╼ 10
            │   └─╼ 11
            └─╼ 9
                ├─╼ 12
                └─╼ 13
        """
    ).strip()
    assert ret == target

    tree3 = nx.balanced_tree(r=2, h=2, create_using=nx.DiGraph)
    forest = nx.disjoint_union_all([tree1, tree2, tree3])
    ret = "\n".join(nx.generate_network_text(forest, sources=[0, 14, 7]))

    target = dedent(
        """
        ╟── 0
        ╎   ├─╼ 1
        ╎   │   ├─╼ 3
        ╎   │   └─╼ 4
        ╎   └─╼ 2
        ╎       ├─╼ 5
        ╎       └─╼ 6
        ╟── 14
        ╎   ├─╼ 15
        ╎   │   ├─╼ 17
        ╎   │   └─╼ 18
        ╎   └─╼ 16
        ╎       ├─╼ 19
        ╎       └─╼ 20
        ╙── 7
            ├─╼ 8
            │   ├─╼ 10
            │   └─╼ 11
            └─╼ 9
                ├─╼ 12
                └─╼ 13
        """
    ).strip()
    assert ret == target

    ret = "\n".join(
        nx.generate_network_text(forest, sources=[0, 14, 7], ascii_only=True)
    )

    target = dedent(
        """
        +-- 0
        :   |-> 1
        :   |   |-> 3
        :   |   L-> 4
        :   L-> 2
        :       |-> 5
        :       L-> 6
        +-- 14
        :   |-> 15
        :   |   |-> 17
        :   |   L-> 18
        :   L-> 16
        :       |-> 19
        :       L-> 20
        +-- 7
            |-> 8
            |   |-> 10
            |   L-> 11
            L-> 9
                |-> 12
                L-> 13
        """
    ).strip()
    assert ret == target

