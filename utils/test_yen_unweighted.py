
def test_yen_unweighted():
    # Ask for more paths than there are, verify only the available paths are returned
    distances, predecessors = yen(
        directed_G,
        source=0,
        sink=3,
        K=4,
        unweighted=True,
        return_predecessors=True,
    )
    assert_allclose(distances, [2., 3.])
    assert_allclose(predecessors, directed_2SP_0_to_3)

