
def test_substitute_dummies_NO_operator():
    i, j = symbols('i j', cls=Dummy)
    assert substitute_dummies(att(i, j)*NO(Fd(i)*F(j))
                - att(j, i)*NO(Fd(j)*F(i))) == 0

