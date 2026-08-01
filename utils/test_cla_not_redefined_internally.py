
def test_cla_not_redefined_internally():
    for klass in Axes.__subclasses__():
        # Check that cla does not get redefined in our Axes subclasses, except
        # for in the above test function.
        if 'test_subclass_clear_cla' not in klass.__qualname__:
            assert 'cla' not in klass.__dict__

