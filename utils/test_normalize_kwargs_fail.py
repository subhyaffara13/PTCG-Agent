
def test_normalize_kwargs_fail(inp, alias_def):

    @_api.define_aliases(alias_def)
    class Type(mpl.artist.Artist):
        def get_a(self): return None

    with pytest.raises(TypeError):
        cbook.normalize_kwargs(inp, Type)

