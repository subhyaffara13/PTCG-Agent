
def test_list_builtin():
    backends = backend_registry.list_builtin()
    assert not has_duplicates(backends)
    # Compare using sets as order is not important
    assert {*backends} == {
        'gtk3agg', 'gtk3cairo', 'gtk4agg', 'gtk4cairo', 'macosx', 'nbagg', 'notebook',
        'qtagg', 'qtcairo', 'qt5agg', 'qt5cairo', 'tkagg',
        'tkcairo', 'webagg', 'wx', 'wxagg', 'wxcairo', 'agg', 'cairo', 'pdf', 'pgf',
        'ps', 'svg', 'template',
    }

