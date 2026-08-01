
def test_clf_not_redefined():
    for klass in FigureBase.__subclasses__():
        # check that subclasses do not get redefined in our Figure subclasses
        assert 'clf' not in klass.__dict__

