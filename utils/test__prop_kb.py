
def test_PropKB():
    A, B, C = symbols('A,B,C')
    kb = PropKB()
    assert kb.ask(A >> B) is False
    assert kb.ask(A >> (B >> A)) is True
    kb.tell(A >> B)
    kb.tell(B >> C)
    assert kb.ask(A) is False
    assert kb.ask(B) is False
    assert kb.ask(C) is False
    assert kb.ask(~A) is False
    assert kb.ask(~B) is False
    assert kb.ask(~C) is False
    assert kb.ask(A >> C) is True
    kb.tell(A)
    assert kb.ask(A) is True
    assert kb.ask(B) is True
    assert kb.ask(C) is True
    assert kb.ask(~C) is False
    kb.retract(A)
    assert kb.ask(C) is False

