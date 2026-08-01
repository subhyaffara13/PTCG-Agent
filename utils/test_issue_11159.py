
def test_issue_11159():
    # Tests Application._eval_subs
    with _exp_is_pow(False):
        expr1 = E
        expr0 = expr1 * expr1
        expr1 = expr0.subs(expr1,expr0)
        assert expr0 == expr1
    with _exp_is_pow(True):
        expr1 = E
        expr0 = expr1 * expr1
        expr2 = expr0.subs(expr1, expr0)
        assert expr2 == E ** 4

