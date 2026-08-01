
def test_issue_24288():
    assert parse_expr("1 < 2", evaluate=False) == Lt(1, 2, evaluate=False)
    assert parse_expr("1 <= 2", evaluate=False) == Le(1, 2, evaluate=False)
    assert parse_expr("1 > 2", evaluate=False) == Gt(1, 2, evaluate=False)
    assert parse_expr("1 >= 2", evaluate=False) == Ge(1, 2, evaluate=False)
    assert parse_expr("1 != 2", evaluate=False) == Ne(1, 2, evaluate=False)
    assert parse_expr("1 == 2", evaluate=False) == Eq(1, 2, evaluate=False)
    assert parse_expr("1 < 2 < 3", evaluate=False) == And(Lt(1, 2, evaluate=False), Lt(2, 3, evaluate=False), evaluate=False)
    assert parse_expr("1 <= 2 <= 3", evaluate=False) == And(Le(1, 2, evaluate=False), Le(2, 3, evaluate=False), evaluate=False)
    assert parse_expr("1 < 2 <= 3 < 4", evaluate=False) == \
        And(Lt(1, 2, evaluate=False), Le(2, 3, evaluate=False), Lt(3, 4, evaluate=False), evaluate=False)
    # Valid Python relational operators that SymPy does not decide how to handle them yet
    raises(ValueError, lambda: parse_expr("1 in 2", evaluate=False))
    raises(ValueError, lambda: parse_expr("1 is 2", evaluate=False))
    raises(ValueError, lambda: parse_expr("1 not in 2", evaluate=False))
    raises(ValueError, lambda: parse_expr("1 is not 2", evaluate=False))

