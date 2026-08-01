
def test_no_offsets_datalim():
    # A collection with no offsets and a non transData
    # transform should return a null bbox
    ax = plt.axes()
    coll = mcollections.PathCollection([mpath.Path([(0, 0), (1, 0)])])
    ax.add_collection(coll)
    coll_data_lim = coll.get_datalim(mtransforms.IdentityTransform())
    assert_array_equal(coll_data_lim.get_points(),
                       mtransforms.Bbox.null().get_points())

