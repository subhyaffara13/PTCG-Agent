
def test_null_collection_datalim():
    col = mcollections.PathCollection([])
    col_data_lim = col.get_datalim(mtransforms.IdentityTransform())
    assert_array_equal(col_data_lim.get_points(),
                       mtransforms.Bbox.null().get_points())

