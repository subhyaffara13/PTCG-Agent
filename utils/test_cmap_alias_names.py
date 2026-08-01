
def test_cmap_alias_names():
    assert matplotlib.colormaps["gray"].name == "gray"  # original
    assert matplotlib.colormaps["grey"].name == "grey"  # alias

