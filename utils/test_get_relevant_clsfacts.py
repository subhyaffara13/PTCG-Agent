
def test_get_relevant_clsfacts():
    exprs = {Abs(x*y)}
    exprs, facts = get_relevant_clsfacts(exprs)
    assert exprs == {x*y}
    assert facts.clauses == \
        {frozenset({Literal(Q.odd(Abs(x*y)), False), Literal(Q.odd(x*y), True)}),
        frozenset({Literal(Q.zero(Abs(x*y)), False), Literal(Q.zero(x*y), True)}),
        frozenset({Literal(Q.even(Abs(x*y)), False), Literal(Q.even(x*y), True)}),
        frozenset({Literal(Q.zero(Abs(x*y)), True), Literal(Q.zero(x*y), False)}),
        frozenset({Literal(Q.even(Abs(x*y)), False),
                    Literal(Q.odd(Abs(x*y)), False),
                    Literal(Q.odd(x*y), True)}),
        frozenset({Literal(Q.even(Abs(x*y)), False),
                    Literal(Q.even(x*y), True),
                    Literal(Q.odd(Abs(x*y)), False)}),
        frozenset({Literal(Q.positive(Abs(x*y)), False),
                    Literal(Q.zero(Abs(x*y)), False)})}

