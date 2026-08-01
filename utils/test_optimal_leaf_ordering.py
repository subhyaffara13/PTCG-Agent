
def test_optimal_leaf_ordering(xp):
    # test with the distance vector y
    Z = optimal_leaf_ordering(xp.asarray(linkage(hierarchy_test_data.ytdist)),
                              xp.asarray(hierarchy_test_data.ytdist))
    expectedZ = hierarchy_test_data.linkage_ytdist_single_olo
    xp_assert_close(Z, xp.asarray(expectedZ), atol=1e-10)

    # test with the observation matrix X
    Z = optimal_leaf_ordering(xp.asarray(linkage(hierarchy_test_data.X, 'ward')),
                              xp.asarray(hierarchy_test_data.X))
    expectedZ = hierarchy_test_data.linkage_X_ward_olo
    xp_assert_close(Z, xp.asarray(expectedZ), atol=1e-06)

