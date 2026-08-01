
def test_operators():
    # Mostly test __and__, __rand__, and so on
    assert True & A == A & True == A
    assert False & A == A & False == False
    assert A & B == And(A, B)
    assert True | A == A | True == True
    assert False | A == A | False == A
    assert A | B == Or(A, B)
    assert ~A == Not(A)
    assert True >> A == A << True == A
    assert False >> A == A << False == True
    assert A >> True == True << A == True
    assert A >> False == False << A == ~A
    assert A >> B == B << A == Implies(A, B)
    assert True ^ A == A ^ True == ~A
    assert False ^ A == A ^ False == A
    assert A ^ B == Xor(A, B)

