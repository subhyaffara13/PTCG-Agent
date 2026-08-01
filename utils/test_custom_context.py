
def test_custom_context():
    """Test ask with custom assumptions context"""
    assert ask(Q.integer(x)) is None
    local_context = AssumptionsContext()
    local_context.add(Q.integer(x))
    assert ask(Q.integer(x), context=local_context) is True
    assert ask(Q.integer(x)) is None

