
def gate_sort(circuit):
    """Sorts the gates while keeping track of commutation relations

    This function uses a bubble sort to rearrange the order of gate
    application. Keeps track of Quantum computations special commutation
    relations (e.g. things that apply to the same Qubit do not commute with
    each other)

    circuit is the Mul of gates that are to be sorted.
    """
    # Make sure we have an Add or Mul.
    if isinstance(circuit, Add):
        return sum(gate_sort(t) for t in circuit.args)
    if isinstance(circuit, Pow):
        return gate_sort(circuit.base)**circuit.exp
    elif isinstance(circuit, Gate):
        return circuit
    if not isinstance(circuit, Mul):
        return circuit

    changes = True
    while changes:
        changes = False
        circ_array = circuit.args
        for i in range(len(circ_array) - 1):
            # Go through each element and switch ones that are in wrong order
            if isinstance(circ_array[i], (Gate, Pow)) and \
                    isinstance(circ_array[i + 1], (Gate, Pow)):
                # If we have a Pow object, look at only the base
                first_base, first_exp = circ_array[i].as_base_exp()
                second_base, second_exp = circ_array[i + 1].as_base_exp()

                # Use SymPy's hash based sorting. This is not mathematical
                # sorting, but is rather based on comparing hashes of objects.
                # See Basic.compare for details.
                if first_base.compare(second_base) > 0:
                    if Commutator(first_base, second_base).doit() == 0:
                        new_args = (circuit.args[:i] + (circuit.args[i + 1],) +
                                   (circuit.args[i],) + circuit.args[i + 2:])
                        circuit = Mul(*new_args)
                        changes = True
                        break
                    if AntiCommutator(first_base, second_base).doit() == 0:
                        new_args = (circuit.args[:i] + (circuit.args[i + 1],) +
                                   (circuit.args[i],) + circuit.args[i + 2:])
                        sign = _S.NegativeOne**(first_exp*second_exp)
                        circuit = sign*Mul(*new_args)
                        changes = True
                        break
    return circuit

