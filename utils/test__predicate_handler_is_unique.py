
def test_Predicate_handler_is_unique():

    # Undefined predicate does not have a handler
    assert Predicate('mypredicate').handler is None

    # Handler of defined predicate is unique to the class
    class MyPredicate(Predicate):
        pass
    mp1 = MyPredicate(Str('mp1'))
    mp2 = MyPredicate(Str('mp2'))
    assert mp1.handler is mp2.handler

