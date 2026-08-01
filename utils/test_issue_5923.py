
def test_issue_5923():
    # most of the issue regarding sympification of args has been handled
    # and is tested internally by the use of args_cnc through the quantum
    # module, but the following is a test from the issue that used to raise.
    assert TensorProduct(1, Qubit('1')*Qubit('1').dual) == \
        TensorProduct(1, OuterProduct(Qubit(1), QubitBra(1)))

