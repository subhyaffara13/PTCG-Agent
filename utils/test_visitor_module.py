
def test_visitor_module(code, expected):
    (
        module_complexity,
        functions_complexity,
        classes_complexity,
        total_complexity,
    ) = expected

    visitor = ComplexityVisitor.from_code(dedent(code))
    assert visitor.complexity, module_complexity
    assert visitor.functions_complexity == functions_complexity
    assert visitor.classes_complexity == classes_complexity
    assert visitor.total_complexity == total_complexity

