
def test_fontproperty_default_cache_invalidation():
    mpl.rcParams["font.weight"] = "normal"
    assert findfont("DejaVu Sans").endswith("DejaVuSans.ttf")
    mpl.rcParams["font.weight"] = "bold"
    assert findfont("DejaVu Sans").endswith("DejaVuSans-Bold.ttf")

