
def test_AssocOp_flatten():
    a, b, c, d = symbols('a,b,c,d')

    class MyAssoc(AssocOp):
        identity = S.One

    assert MyAssoc(a, MyAssoc(b, c)).args == \
        MyAssoc(MyAssoc(a, b), c).args == \
        MyAssoc(MyAssoc(a, b, c)).args == \
        MyAssoc(a, b, c).args == \
            (a, b, c)
    u = MyAssoc(b, c)
    v = MyAssoc(u, d, evaluate=False)
    assert v.args == (u, d)
    # like Add, any unevaluated outer call will flatten inner args
    assert MyAssoc(a, v).args == (a, b, c, d)

