
def test_StateSpace_functions():
    # https://in.mathworks.com/help/control/ref/statespacemodel.obsv.html

    A_mat = Matrix([[-1.5, -2], [1, 0]])
    B_mat = Matrix([0.5, 0])
    C_mat = Matrix([[0, 1]])
    D_mat = Matrix([1])
    SS1 = StateSpace(A_mat, B_mat, C_mat, D_mat)
    SS2 = StateSpace(Matrix([[1, 1], [4, -2]]),Matrix([[0, 1], [0, 2]]),Matrix([[-1, 1], [1, -1]]))
    SS3 = StateSpace(Matrix([[1, 1], [4, -2]]),Matrix([[1, -1], [1, -1]]))
    SS4 = StateSpace(Matrix([[a0, a1], [a2, a3]]), Matrix([[b1], [b2]]), Matrix([[c1, c2]]))

    # Observability
    assert SS1.is_observable() == True
    assert SS2.is_observable() == False
    assert SS1.observability_matrix() == Matrix([[0, 1], [1, 0]])
    assert SS2.observability_matrix() == Matrix([[-1,  1], [ 1, -1], [ 3, -3], [-3,  3]])
    assert SS1.observable_subspace() == [Matrix([[0], [1]]), Matrix([[1], [0]])]
    assert SS2.observable_subspace() == [Matrix([[-1], [ 1], [ 3], [-3]])]
    Qo = SS4.observability_matrix().subs([(a0, 0), (a1, -6), (a2, 1), (a3, -5), (c1, 0), (c2, 1)])
    assert Qo == Matrix([[0, 1], [1, -5]])

    # Controllability
    assert SS1.is_controllable() == True
    assert SS3.is_controllable() == False
    assert SS1.controllability_matrix() ==  Matrix([[0.5, -0.75], [  0,   0.5]])
    assert SS3.controllability_matrix() == Matrix([[1, -1, 2, -2], [1, -1, 2, -2]])
    assert SS1.controllable_subspace() == [Matrix([[0.5], [  0]]), Matrix([[-0.75], [  0.5]])]
    assert SS3.controllable_subspace() == [Matrix([[1], [1]])]
    assert SS4.controllable_subspace() == [Matrix([
                                          [b1],
                                          [b2]]), Matrix([
                                          [a0*b1 + a1*b2],
                                          [a2*b1 + a3*b2]])]
    Qc = SS4.controllability_matrix().subs([(a0, 0), (a1, 1), (a2, -6), (a3, -5), (b1, 0), (b2, 1)])
    assert Qc == Matrix([[0, 1], [1, -5]])

    # Append
    A1 = Matrix([[0, 1], [1, 0]])
    B1 = Matrix([[0], [1]])
    C1 = Matrix([[0, 1]])
    D1 = Matrix([[0]])
    ss1 = StateSpace(A1, B1, C1, D1)
    ss2 = StateSpace(Matrix([[1, 0], [0, 1]]), Matrix([[1], [0]]), Matrix([[1, 0]]), Matrix([[1]]))
    ss3 = ss1.append(ss2)
    ss4 = SS4.append(ss1)

    assert ss3.num_states == ss1.num_states + ss2.num_states
    assert ss3.num_inputs == ss1.num_inputs + ss2.num_inputs
    assert ss3.num_outputs == ss1.num_outputs + ss2.num_outputs
    assert ss3.state_matrix == Matrix([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    assert ss3.input_matrix == Matrix([[0, 0], [1, 0], [0, 1], [0, 0]])
    assert ss3.output_matrix == Matrix([[0, 1, 0, 0], [0, 0, 1, 0]])
    assert ss3.feedforward_matrix == Matrix([[0, 0], [0, 1]])

    # Using symbolic matrices
    assert ss4.num_states == SS4.num_states + ss1.num_states
    assert ss4.num_inputs == SS4.num_inputs + ss1.num_inputs
    assert ss4.num_outputs == SS4.num_outputs + ss1.num_outputs
    assert ss4.state_matrix == Matrix([[a0, a1, 0, 0], [a2, a3, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    assert ss4.input_matrix == Matrix([[b1, 0], [b2, 0], [0, 0], [0, 1]])
    assert ss4.output_matrix == Matrix([[c1, c2, 0, 0], [0, 0, 0, 1]])
    assert ss4.feedforward_matrix == Matrix([[0, 0], [0, 0]])

