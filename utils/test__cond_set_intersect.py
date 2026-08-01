
def test_CondSet_intersect():
    input_conditionset = ConditionSet(x, x**2 > 4, Interval(1, 4, False,
        False))
    other_domain = Interval(0, 3, False, False)
    output_conditionset = ConditionSet(x, x**2 > 4, Interval(
        1, 3, False, False))
    assert Intersection(input_conditionset, other_domain
        ) == output_conditionset

