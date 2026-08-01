
def test_performance_of_adding_order():
    l = [x**i for i in range(1000)]
    l.append(O(x**1001))
    assert Add(*l).subs(x,1) == O(1)

