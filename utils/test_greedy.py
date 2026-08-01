
def test_greedy():
    tree = [inc, (dec, double)]  # either inc or dec-then-double

    fn = greedy(tree, objective=lambda x: -x)
    assert fn(4) == 6  # highest value comes from the dec then double
    assert fn(1) == 2  # highest value comes from the inc

    tree = [inc, dec, [inc, dec, [(inc, inc), (dec, dec)]]]
    lowest = greedy(tree)
    assert lowest(10) == 8

    highest = greedy(tree, objective=lambda x: -x)
    assert highest(10) == 12

