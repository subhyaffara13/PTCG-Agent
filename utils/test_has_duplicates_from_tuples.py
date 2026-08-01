
def test_has_duplicates_from_tuples():
    # GH 9075
    t = [
        ("x", "out", "z", 5, "y", "in", "z", 169),
        ("x", "out", "z", 7, "y", "in", "z", 119),
        ("x", "out", "z", 9, "y", "in", "z", 135),
        ("x", "out", "z", 13, "y", "in", "z", 145),
        ("x", "out", "z", 14, "y", "in", "z", 158),
        ("x", "out", "z", 16, "y", "in", "z", 122),
        ("x", "out", "z", 17, "y", "in", "z", 160),
        ("x", "out", "z", 18, "y", "in", "z", 180),
        ("x", "out", "z", 20, "y", "in", "z", 143),
        ("x", "out", "z", 21, "y", "in", "z", 128),
        ("x", "out", "z", 22, "y", "in", "z", 129),
        ("x", "out", "z", 25, "y", "in", "z", 111),
        ("x", "out", "z", 28, "y", "in", "z", 114),
        ("x", "out", "z", 29, "y", "in", "z", 121),
        ("x", "out", "z", 31, "y", "in", "z", 126),
        ("x", "out", "z", 32, "y", "in", "z", 155),
        ("x", "out", "z", 33, "y", "in", "z", 123),
        ("x", "out", "z", 12, "y", "in", "z", 144),
    ]

    mi = MultiIndex.from_tuples(t)
    assert not mi.has_duplicates

