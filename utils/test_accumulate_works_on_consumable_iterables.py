
def test_accumulate_works_on_consumable_iterables():
    assert list(accumulate(add, iter((1, 2, 3)))) == [1, 3, 6]

