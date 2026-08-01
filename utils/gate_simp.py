
def gate_simp(circuit):
    """Simplifies gates symbolically

    It first sorts gates using gate_sort. It then applies basic
    simplification rules to the circuit, e.g., XGate**2 = Identity
    """

    # Bubble sort out gates that commute.
    circuit = gate_sort(circuit)

    # Do simplifications by subing a simplification into the first element
    # which can be simplified. We recursively call gate_simp with new circuit
    # as input more simplifications exist.
    if isinstance(circuit, Add):
        return sum(gate_simp(t) for t in circuit.args)
    elif isinstance(circuit, Mul):
        circuit_args = circuit.args
    elif isinstance(circuit, Pow):
        b, e = circuit.as_base_exp()
        circuit_args = (gate_simp(b)**e,)
    else:
        return circuit

    # Iterate through each element in circuit, simplify if possible.
    for i in range(len(circuit_args)):
        # H,X,Y or Z squared is 1.
        # T**2 = S, S**2 = Z
        if isinstance(circuit_args[i], Pow):
            if isinstance(circuit_args[i].base,
                (HadamardGate, XGate, YGate, ZGate)) \
                    and isinstance(circuit_args[i].exp, Number):
                # Build a new circuit taking replacing the
                # H,X,Y,Z squared with one.
                newargs = (circuit_args[:i] +
                          (circuit_args[i].base**(circuit_args[i].exp % 2),) +
                           circuit_args[i + 1:])
                # Recursively simplify the new circuit.
                circuit = gate_simp(Mul(*newargs))
                break
            elif isinstance(circuit_args[i].base, PhaseGate):
                # Build a new circuit taking old circuit but splicing
                # in simplification.
                newargs = circuit_args[:i]
                # Replace PhaseGate**2 with ZGate.
                newargs = newargs + (ZGate(circuit_args[i].base.args[0])**
                (Integer(circuit_args[i].exp/2)), circuit_args[i].base**
                (circuit_args[i].exp % 2))
                # Append the last elements.
                newargs = newargs + circuit_args[i + 1:]
                # Recursively simplify the new circuit.
                circuit = gate_simp(Mul(*newargs))
                break
            elif isinstance(circuit_args[i].base, TGate):
                # Build a new circuit taking all the old elements.
                newargs = circuit_args[:i]

                # Put an Phasegate in place of any TGate**2.
                newargs = newargs + (PhaseGate(circuit_args[i].base.args[0])**
                Integer(circuit_args[i].exp/2), circuit_args[i].base**
                    (circuit_args[i].exp % 2))

                # Append the last elements.
                newargs = newargs + circuit_args[i + 1:]
                # Recursively simplify the new circuit.
                circuit = gate_simp(Mul(*newargs))
                break
    return circuit

