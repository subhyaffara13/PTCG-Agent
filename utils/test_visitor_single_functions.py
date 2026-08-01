
def test_visitor_single_functions(code, expected):
    visitor = ComplexityVisitor.from_code(dedent(code))
    assert len(visitor.functions) == 1
    assert (visitor.complexity, visitor.functions[0].complexity) == expected

