
def test_all_predicates():
    for fact in _assume_defined:
        method_name = f'_eval_is_{fact}'
        assert hasattr(AssumptionsWrapper, method_name)

