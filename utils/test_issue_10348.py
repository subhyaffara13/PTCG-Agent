
def test_issue_10348():
    u = dynamicsymbols('u:3')
    I = ReferenceFrame('I')
    I.orientnew('A', 'space', u, 'XYZ')

