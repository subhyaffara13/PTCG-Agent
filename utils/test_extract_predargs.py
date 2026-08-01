
def test_extract_predargs():
    props = CNF.from_prop(Q.zero(Abs(x*y)) & Q.zero(x*y))
    assump = CNF.from_prop(Q.zero(x))
    context = CNF.from_prop(Q.zero(y))
    assert extract_predargs(props) == {Abs(x*y), x*y}
    assert extract_predargs(props, assump) == {Abs(x*y), x*y, x}
    assert extract_predargs(props, assump, context) == {Abs(x*y), x*y, x, y}

    props = CNF.from_prop(Eq(x, y))
    assump = CNF.from_prop(Gt(y, z))
    assert extract_predargs(props, assump) == {x, y, z}

