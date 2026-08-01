
def test_cnot():
    """Test a simple cnot circuit. Right now this only makes sure the code doesn't
    raise an exception, and some simple properties
    """
    if not mpl:
        skip("matplotlib not installed")
    else:
        from sympy.physics.quantum.circuitplot import CircuitPlot

    c = CircuitPlot(CNOT(1,0),2,labels=labeller(2))
    assert c.ngates == 2
    assert c.nqubits == 2
    assert c.labels == ['q_1', 'q_0']

    c = CircuitPlot(CNOT(1,0),2)
    assert c.ngates == 2
    assert c.nqubits == 2
    assert c.labels == []

