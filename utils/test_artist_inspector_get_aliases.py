
def test_artist_inspector_get_aliases():
    # test the correct format and type of get_aliases method
    ai = martist.ArtistInspector(mlines.Line2D)
    aliases = ai.get_aliases()
    assert aliases["linewidth"] == {"lw"}

