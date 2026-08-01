
def test_callbackregistry_signals():
    cr = cbook.CallbackRegistry(signals=["foo"])
    results = []
    def cb(x): results.append(x)
    cr.connect("foo", cb)
    with pytest.raises(ValueError):
        cr.connect("bar", cb)
    cr.process("foo", 1)
    with pytest.raises(ValueError):
        cr.process("bar", 1)
    assert results == [1]

