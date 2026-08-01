
def test_yen_directed():
    distances, predecessors = yen(
                            directed_G,
                            source=0,
                            sink=3,
                            K=2,
                            return_predecessors=True
                        )
    assert_allclose(distances, [5., 9.])
    assert_allclose(predecessors, directed_2SP_0_to_3)

