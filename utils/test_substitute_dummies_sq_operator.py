
def test_substitute_dummies_SQ_operator():
    i, j = symbols('i j', cls=Dummy)
    assert substitute_dummies(att(i, j)*Fd(i)*F(j)
                - att(j, i)*Fd(j)*F(i)) == 0

