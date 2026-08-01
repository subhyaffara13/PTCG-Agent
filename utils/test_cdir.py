
def test_cdir():
    assert abs(x).series(x, 0, cdir=1) == x
    assert abs(x).series(x, 0, cdir=-1) == -x
    assert floor(x + 2).series(x, 0, cdir=1) == 2
    assert floor(x + 2).series(x, 0, cdir=-1) == 1
    assert floor(x + 2.2).series(x, 0, cdir=1) == 2
    assert ceiling(x + 2.2).series(x, 0, cdir=-1) == 3
    assert sin(x + y).series(x, 0, cdir=-1) == sin(x + y).series(x, 0, cdir=1)

