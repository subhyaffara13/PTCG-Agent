
def test_visitor(code, expected):
    visitor = HalsteadVisitor.from_code(dedent(code))
    assert expected == (
        visitor.operators,
        visitor.operands,
        visitor.distinct_operators,
        visitor.distinct_operands,
    )

