
def test_visitor_closures(code, closure_names, expected):
    visitor = ComplexityVisitor.from_code(dedent(code))
    func = visitor.functions[0]
    closure_names = closure_names
    expected_cs_cc = expected[:-1]
    expected_total_cc = expected[-1]

    assert len(visitor.functions) == 1

    names = tuple(cs.name for cs in func.closures)
    assert names == closure_names

    cs_complexity = tuple(cs.complexity for cs in func.closures)
    assert cs_complexity == expected_cs_cc
    assert func.complexity == expected_total_cc

    # There was a bug for which `blocks` increased while it got accessed
    v = visitor
    assert v.blocks == v.blocks == v.blocks

