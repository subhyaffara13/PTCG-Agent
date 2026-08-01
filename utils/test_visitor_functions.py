
def test_visitor_functions(code, expected):
    visitor = ComplexityVisitor.from_code(dedent(code))
    assert len(visitor.functions) == len(expected)
    assert tuple(map(GET_COMPLEXITY, visitor.functions)) == expected

