
def test_issue_3979():
    # when this passes, delete this and change the [1:2]
    # to [:2] in the test_hash above for issue 3979
    cls = classes[0]
    raises(AttributeError, lambda: hash(cls.eye(1)))

