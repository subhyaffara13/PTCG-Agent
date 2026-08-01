
def test_ex1():
    if not mpl:
        skip("matplotlib not installed")
    else:
        from sympy.physics.quantum.circuitplot import CircuitPlot

    c = CircuitPlot(CNOT(1,0)*H(1),2,labels=labeller(2))
    assert c.ngates == 2
    assert c.nqubits == 2
    assert c.labels == ['q_1', 'q_0']

