import math


def test_pool():
    with Pool(2) as p:
        p.map(math.sin, [1, 2, 3, 4])

