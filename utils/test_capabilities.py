
def test_capabilities():
    caps = info.capabilities()
    assert caps["boolean indexing"] is True
    assert caps["data-dependent shapes"] is True

