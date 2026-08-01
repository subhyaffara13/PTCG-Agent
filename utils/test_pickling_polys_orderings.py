
def test_pickling_polys_orderings():
    from sympy.polys.orderings import (LexOrder, GradedLexOrder,
        ReversedGradedLexOrder, InverseOrder)
    # from sympy.polys.orderings import ProductOrder

    for c in (LexOrder, LexOrder()):
        check(c)

    for c in (GradedLexOrder, GradedLexOrder()):
        check(c)

    for c in (ReversedGradedLexOrder, ReversedGradedLexOrder()):
        check(c)

    # TODO: Argh, Python is so naive. No lambdas nor inner function support in
    # pickling module. Maybe someone could figure out what to do with this.
    #
    # for c in (ProductOrder, ProductOrder((LexOrder(),       lambda m: m[:2]),
    #                                      (GradedLexOrder(), lambda m: m[2:]))):
    #     check(c)

    for c in (InverseOrder, InverseOrder(LexOrder())):
        check(c)

