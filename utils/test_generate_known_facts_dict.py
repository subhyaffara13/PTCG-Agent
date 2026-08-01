
def test_generate_known_facts_dict():
    known_facts = And(Implies(Q.integer(x), Q.rational(x)),
                      Implies(Q.rational(x), Q.real(x)),
                      Implies(Q.real(x), Q.complex(x)))
    known_facts_keys = {Q.integer(x), Q.rational(x), Q.real(x), Q.complex(x)}

    assert generate_known_facts_dict(known_facts_keys, known_facts) == \
        {Q.complex: ({Q.complex}, set()),
         Q.integer: ({Q.complex, Q.integer, Q.rational, Q.real}, set()),
         Q.rational: ({Q.complex, Q.rational, Q.real}, set()),
         Q.real: ({Q.complex, Q.real}, set())}

