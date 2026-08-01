
def test_hardcoded():
    # define a test problem
    edges_1 = [
        ("a", "b"),
        ("a", "c"),
        ("a", "d"),
        ("b", "e"),
        ("b", "f"),
        ("e", "j"),
        ("e", "k"),
        ("c", "g"),
        ("c", "h"),
        ("g", "m"),
        ("d", "i"),
        ("f", "l"),
    ]

    edges_2 = [
        ("v", "y"),
        ("v", "z"),
        ("u", "x"),
        ("q", "u"),
        ("q", "v"),
        ("p", "t"),
        ("n", "p"),
        ("n", "q"),
        ("n", "o"),
        ("o", "r"),
        ("o", "s"),
        ("s", "w"),
    ]

    # there are two possible correct isomorphisms
    # it currently returns isomorphism1
    # but the second is also correct
    isomorphism1 = [
        ("a", "n"),
        ("b", "q"),
        ("c", "o"),
        ("d", "p"),
        ("e", "v"),
        ("f", "u"),
        ("g", "s"),
        ("h", "r"),
        ("i", "t"),
        ("j", "y"),
        ("k", "z"),
        ("l", "x"),
        ("m", "w"),
    ]

    # could swap y and z
    isomorphism2 = [
        ("a", "n"),
        ("b", "q"),
        ("c", "o"),
        ("d", "p"),
        ("e", "v"),
        ("f", "u"),
        ("g", "s"),
        ("h", "r"),
        ("i", "t"),
        ("j", "z"),
        ("k", "y"),
        ("l", "x"),
        ("m", "w"),
    ]

    t1 = nx.Graph()
    t1.add_edges_from(edges_1)
    root1 = "a"

    t2 = nx.Graph()
    t2.add_edges_from(edges_2)
    root2 = "n"

    isomorphism = sorted(nx.isomorphism.rooted_tree_isomorphism(t1, root1, t2, root2))

    # is correct by hand
    assert isomorphism in (isomorphism1, isomorphism2)

    # check algorithmically
    assert _check_isomorphism(t1, t2, isomorphism)

    # try again as digraph
    t1 = nx.DiGraph()
    t1.add_edges_from(edges_1)
    root1 = "a"

    t2 = nx.DiGraph()
    t2.add_edges_from(edges_2)
    root2 = "n"

    isomorphism = sorted(nx.isomorphism.rooted_tree_isomorphism(t1, root1, t2, root2))

    # is correct by hand
    assert isomorphism in (isomorphism1, isomorphism2)

    # check algorithmically
    assert _check_isomorphism(t1, t2, isomorphism)

