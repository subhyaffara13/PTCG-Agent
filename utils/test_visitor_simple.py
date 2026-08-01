
def test_visitor_simple(code, expected, kwargs):
    visitor = ComplexityVisitor.from_code(dedent(code), **kwargs)
    assert visitor.complexity == expected

