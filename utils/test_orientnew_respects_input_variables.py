
def test_orientnew_respects_input_variables():
    N = ReferenceFrame('N')
    q1 = dynamicsymbols('q1')
    A = N.orientnew('a', 'Axis', [q1, N.z])

    #build non-standard variable names
    name = 'b'
    new_variables = ['notb_'+x+'1' for x in N.indices]
    B = N.orientnew(name, 'Axis', [q1, N.z], variables=new_variables)

    for j,var in enumerate(A.varlist):
        assert var.name == A.name + '_' + A.indices[j]

    for j,var in enumerate(B.varlist):
        assert var.name == new_variables[j]

