
def test_dir():
    assert abs(x).series(x, 0, dir="+") == x
    assert abs(x).series(x, 0, dir="-") == -x
    assert floor(x + 2).series(x, 0, dir='+') == 2
    assert floor(x + 2).series(x, 0, dir='-') == 1
    assert floor(x + 2.2).series(x, 0, dir='-') == 2
    assert ceiling(x + 2.2).series(x, 0, dir='-') == 3
    assert sin(x + y).series(x, 0, dir='-') == sin(x + y).series(x, 0, dir='+')


def test_dir():
    # GH#27571 dir(interval_index) should not raise
    index = IntervalIndex.from_arrays([0, 1], [1, 2])
    result = dir(index)
    assert "str" not in result

