
def test_tarjan():
    G = tarjan_bridge_graph()

    aug_edges = set(_augment_and_check(G, k=2)[0])
    print(f"aug_edges = {aug_edges!r}")
    # can't assert edge exactly equality due to non-determinant edge order
    # but we do know the size of the solution must be 3
    assert len(aug_edges) == 3

    avail = [
        (9, 7),
        (8, 5),
        (2, 10),
        (6, 13),
        (11, 18),
        (1, 17),
        (2, 3),
        (16, 17),
        (18, 14),
        (15, 14),
    ]
    aug_edges = set(_augment_and_check(G, avail=avail, k=2)[0])

    # Can't assert exact length since approximation depends on the order of a
    # dict traversal.
    assert len(aug_edges) <= 3 * 2

    _check_augmentations(G, avail)

