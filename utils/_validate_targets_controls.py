
def _validate_targets_controls(tandc):
    tandc = list(tandc)
    # Check for integers
    for bit in tandc:
        if not bit.is_Integer and not bit.is_Symbol:
            raise TypeError('Integer expected, got: %r' % tandc[bit])
    # Detect duplicates
    if len(set(tandc)) != len(tandc):
        raise QuantumError(
            'Target/control qubits in a gate cannot be duplicated'
        )

