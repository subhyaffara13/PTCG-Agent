
def test_satisfiable_all_models():
    from sympy.abc import A, B
    assert next(satisfiable(False, all_models=True)) is False
    assert list(satisfiable((A >> ~A) & A, all_models=True)) == [False]
    assert list(satisfiable(True, all_models=True)) == [{true: true}]

    models = [{A: True, B: False}, {A: False, B: True}]
    result = satisfiable(A ^ B, all_models=True)
    models.remove(next(result))
    models.remove(next(result))
    raises(StopIteration, lambda: next(result))
    assert not models

    assert list(satisfiable(Equivalent(A, B), all_models=True)) == \
    [{A: False, B: False}, {A: True, B: True}]

    models = [{A: False, B: False}, {A: False, B: True}, {A: True, B: True}]
    for model in satisfiable(A >> B, all_models=True):
        models.remove(model)
    assert not models

    # This is a santiy test to check that only the required number
    # of solutions are generated. The expr below has 2**100 - 1 models
    # which would time out the test if all are generated at once.
    from sympy.utilities.iterables import numbered_symbols
    from sympy.logic.boolalg import Or
    sym = numbered_symbols()
    X = [next(sym) for i in range(100)]
    result = satisfiable(Or(*X), all_models=True)
    for i in range(10):
        assert next(result)

