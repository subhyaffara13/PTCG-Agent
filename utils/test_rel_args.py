
def test_rel_args():
    # can't have Boolean args; this is automatic for True/False
    # with Python 3 and we confirm that SymPy does the same
    # for true/false
    for op in ['<', '<=', '>', '>=']:
        for b in (S.true, x < 1, And(x, y)):
            for v in (0.1, 1, 2**32, t, S.One):
                raises(TypeError, lambda: Relational(b, v, op))

