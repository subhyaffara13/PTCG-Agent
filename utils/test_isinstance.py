
def test_isinstance():
    objects = [(), {}, m.Pet("Polly", "parrot")] + [m.Dog("Molly")] * 4
    expected = (True, True, True, True, True, False, False)
    assert m.check_instances(objects) == expected


def test_isinstance():
    assert m.isinstance_untyped(np.array([1, 2, 3]), "not an array")
    assert m.isinstance_typed(np.array([1.0, 2.0, 3.0]))

