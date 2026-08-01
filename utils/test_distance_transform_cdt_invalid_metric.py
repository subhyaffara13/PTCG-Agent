
def test_distance_transform_cdt_invalid_metric(xp):
    msg = 'invalid metric provided'
    with pytest.raises(ValueError, match=msg):
        ndimage.distance_transform_cdt(xp.ones((5, 5)),
                                       metric="garbage")

