
def test_polygon_selector_clear_method(ax):
    onselect = mock.Mock(spec=noop, return_value=None)
    tool = widgets.PolygonSelector(ax, onselect)

    for result in ([(50, 50), (150, 50), (50, 150), (50, 50)],
                   [(50, 50), (100, 50), (50, 150), (50, 50)]):
        for xy in result:
            for event in polygon_place_vertex(ax, xy):
                event._process()

        artist = tool._selection_artist

        assert tool._selection_completed
        assert tool.get_visible()
        assert artist.get_visible()
        np.testing.assert_equal(artist.get_xydata(), result)
        assert onselect.call_args == ((result[:-1],), {})

        tool.clear()
        assert not tool._selection_completed
        np.testing.assert_equal(artist.get_xydata(), [(0, 0)])

