import random

def test_apply_represent_equality():
    gates = [HadamardGate(int(3*random.random())),
     XGate(int(3*random.random())), ZGate(int(3*random.random())),
        YGate(int(3*random.random())), ZGate(int(3*random.random())),
        PhaseGate(int(3*random.random()))]

    circuit = Qubit(int(random.random()*2), int(random.random()*2),
    int(random.random()*2), int(random.random()*2), int(random.random()*2),
        int(random.random()*2))
    for i in range(int(random.random()*6)):
        circuit = gates[int(random.random()*6)]*circuit

    mat = represent(circuit, nqubits=6)
    states = qapply(circuit)
    state_rep = matrix_to_qubit(mat)
    states = states.expand()
    state_rep = state_rep.expand()
    assert state_rep == states

