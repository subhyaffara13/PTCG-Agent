
def test_single_fact_lookup():
    known_facts = And(Implies(Q.integer, Q.rational),
                      Implies(Q.rational, Q.real),
                      Implies(Q.real, Q.complex))
    known_facts_keys = {Q.integer, Q.rational, Q.real, Q.complex}

    known_facts_cnf = to_cnf(known_facts)
    mapping = single_fact_lookup(known_facts_keys, known_facts_cnf)

    assert mapping[Q.rational] == {Q.real, Q.rational, Q.complex}

