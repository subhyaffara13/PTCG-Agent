
def test_ex4():
    if not mpl:
        skip("matplotlib not installed")
    else:
        from sympy.physics.quantum.circuitplot import CircuitPlot

    c = CircuitPlot(SWAP(0,2)*H(0)* CGate((0,),S(1)) *H(1)*CGate((0,),T(2))\
                    *CGate((1,),S(2))*H(2),3,labels=labeller(3,'j'))
    assert c.ngates == 7
    assert c.nqubits == 3
    assert c.labels == ['j_2', 'j_1', 'j_0']

