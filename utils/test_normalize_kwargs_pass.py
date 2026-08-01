
def test_normalize_kwargs_pass(inp, expected, alias_def):

    @_api.define_aliases(alias_def)
    class Type(mpl.artist.Artist):
        def get_a(self): return None

    assert expected == cbook.normalize_kwargs(inp, Type)
    old_alias_map = {}
    for alias, prop in Type._alias_to_prop.items():
        old_alias_map.setdefault(prop, []).append(alias)
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        assert expected == cbook.normalize_kwargs(inp, old_alias_map)

