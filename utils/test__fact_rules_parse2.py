
def test_FactRules_parse2():
    raises(ValueError, lambda: FactRules('a -> !a'))

