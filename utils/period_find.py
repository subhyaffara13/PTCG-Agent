
def period_find(a, N):
    """Finds the period of a in modulo N arithmetic

    This is quantum part of Shor's algorithm. It takes two registers,
    puts first in superposition of states with Hadamards so: ``|k>|0>``
    with k being all possible choices. It then does a controlled mod and
    a QFT to determine the order of a.
    """
    epsilon = .5
    # picks out t's such that maintains accuracy within epsilon
    t = int(2*math.ceil(log(N, 2)))
    # make the first half of register be 0's |000...000>
    start = [0 for x in range(t)]
    # Put second half into superposition of states so we have |1>x|0> + |2>x|0> + ... |k>x>|0> + ... + |2**n-1>x|0>
    factor = 1/sqrt(2**t)
    qubits = 0
    for arr in variations(range(2), t, repetition=True):
        qbitArray = list(arr) + start
        qubits = qubits + Qubit(*qbitArray)
    circuit = (factor*qubits).expand()
    # Controlled second half of register so that we have:
    # |1>x|a**1 %N> + |2>x|a**2 %N> + ... + |k>x|a**k %N >+ ... + |2**n-1=k>x|a**k % n>
    circuit = CMod(t, a, N)*circuit
    # will measure first half of register giving one of the a**k%N's

    circuit = qapply(circuit)
    for i in range(t):
        circuit = measure_partial_oneshot(circuit, i)
    # Now apply Inverse Quantum Fourier Transform on the second half of the register

    circuit = qapply(QFT(t, t*2).decompose()*circuit, floatingPoint=True)
    for i in range(t):
        circuit = measure_partial_oneshot(circuit, i + t)
    if isinstance(circuit, Qubit):
        register = circuit
    elif isinstance(circuit, Mul):
        register = circuit.args[-1]
    else:
        register = circuit.args[-1].args[-1]

    n = 1
    answer = 0
    for i in range(len(register)/2):
        answer += n*register[i + t]
        n = n << 1
    if answer == 0:
        raise OrderFindingException(
            "Order finder returned 0. Happens with chance %f" % epsilon)
    #turn answer into r using continued fractions
    g = getr(answer, 2**t, N)
    return g

