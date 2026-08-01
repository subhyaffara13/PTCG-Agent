
def test_mutable_fontproperty_cache_invalidation():
    fp = FontProperties()
    assert findfont(fp).endswith("DejaVuSans.ttf")
    fp.set_weight("bold")
    assert findfont(fp).endswith("DejaVuSans-Bold.ttf")

