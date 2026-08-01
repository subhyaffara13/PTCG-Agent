
def test_visitor_classes(code, expected):
    total_class_complexity = expected[0]
    methods_complexity = expected[1:]
    visitor = ComplexityVisitor.from_code(dedent(code))
    assert len(visitor.classes) == 1
    assert len(visitor.functions) == 0
    cls = visitor.classes[0]
    assert cls.real_complexity == total_class_complexity
    assert tuple(map(GET_COMPLEXITY, cls.methods)) == methods_complexity

