
def test_abc_non_local():
    assert dill.copy(OneTwoThree) is not OneTwoThree
    assert dill.copy(EasyAsAbc) is not EasyAsAbc

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", dill.PicklingWarning)
        assert dill.copy(OneTwoThree, byref=True) is OneTwoThree
        assert dill.copy(EasyAsAbc, byref=True) is EasyAsAbc

    instance = EasyAsAbc()
    # Set a property that StockPickle can't preserve
    instance.bar = lambda x: x**2
    depickled = dill.copy(instance)
    assert type(depickled) is type(instance) #NOTE: issue #612, test_abc_local
    #NOTE: dill.copy of local (or non-local) classes should (not) be the same?
    assert type(depickled.bar) is FunctionType
    assert depickled.bar(3) == 9
    assert depickled.sfoo() == "Static Method SFOO"
    assert depickled.cfoo() == "Class Method CFOO"
    assert depickled.foo() == "Instance Method FOO"

