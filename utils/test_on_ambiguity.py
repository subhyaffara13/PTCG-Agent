
def test_on_ambiguity():
    f = Dispatcher('f')

    def identity(x): return x

    ambiguities = [False]

    def on_ambiguity(dispatcher, amb):
        ambiguities[0] = True

    f.add((object, object), identity, on_ambiguity=on_ambiguity)
    assert not ambiguities[0]
    f.add((object, float), identity, on_ambiguity=on_ambiguity)
    assert not ambiguities[0]
    f.add((float, object), identity, on_ambiguity=on_ambiguity)
    assert ambiguities[0]

