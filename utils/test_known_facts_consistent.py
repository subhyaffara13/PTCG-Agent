
def test_known_facts_consistent():
    """"Test that ask_generated.py is up-to-date"""
    x = Symbol('x')
    fact = get_known_facts(x)
    # test cnf clauses of fact between unary predicates
    cnf = CNF.to_CNF(fact)
    clauses = set()
    clauses.update(frozenset(Literal(lit.arg.function, lit.is_Not) for lit in sorted(cl, key=str)) for cl in cnf.clauses)
    assert get_all_known_facts() == clauses
    # test dictionary of fact between unary predicates
    keys = [pred(x) for pred in get_known_facts_keys()]
    mapping = generate_known_facts_dict(keys, fact)
    assert get_known_facts_dict() == mapping

