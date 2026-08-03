from pathlib import Path


def test_clipping_full():
    p = Path([[1e30, 1e30]] * 5)
    simplified = list(p.iter_segments(clip=[0, 0, 100, 100]))
    assert simplified == []

    p = Path([[50, 40], [75, 65]], [1, 2])
    simplified = list(p.iter_segments(clip=[0, 0, 100, 100]))
    assert ([(list(x), y) for x, y in simplified] ==
            [([50, 40], 1), ([75, 65], 2)])

    p = Path([[50, 40]], [1])
    simplified = list(p.iter_segments(clip=[0, 0, 100, 100]))
    assert ([(list(x), y) for x, y in simplified] ==
            [([50, 40], 1)])

