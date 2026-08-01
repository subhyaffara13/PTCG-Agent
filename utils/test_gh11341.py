
def test_gh11341():
    # gh-11341 noted that these three constants should exist (for backward
    # compatibility) and should always have the same value:
    a = constants.epsilon_0
    b = constants.physical_constants['electric constant'][0]
    c = constants.physical_constants['vacuum electric permittivity'][0]
    assert a == b == c

