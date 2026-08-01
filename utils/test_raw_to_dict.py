
def test_raw_to_dict():
    assert tools.raw_to_dict(Module(103, 123, 98, 8, 19, 5, 3)) == {
        'loc': 103,
        'lloc': 123,
        'sloc': 98,
        'comments': 8,
        'multi': 19,
        'blank': 5,
        'single_comments': 3,
    }

