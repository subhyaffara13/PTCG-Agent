
def test_topk_is_stable():
    assert topk(4, [5, 9, 2, 1, 5, 3], key=lambda x: 1) == (5, 9, 2, 1)

