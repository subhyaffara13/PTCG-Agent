
def test_meijerg_period():
    assert meijerg([], [1], [0], [], x).get_period() == 2*pi
    assert meijerg([1], [], [], [0], x).get_period() == 2*pi
    assert meijerg([], [], [0], [], x).get_period() == 2*pi  # exp(x)
    assert meijerg(
        [], [], [0], [S.Half], x).get_period() == 2*pi  # cos(sqrt(x))
    assert meijerg(
        [], [], [S.Half], [0], x).get_period() == 4*pi  # sin(sqrt(x))
    assert meijerg([1, 1], [], [1], [0], x).get_period() is oo  # log(1 + x)

