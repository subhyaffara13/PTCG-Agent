
def test_eval_empty_globals():
    assert "__builtins__" in m.eval_empty_globals(None)

    g = {}
    assert "__builtins__" in m.eval_empty_globals(g)
    assert "__builtins__" in g

