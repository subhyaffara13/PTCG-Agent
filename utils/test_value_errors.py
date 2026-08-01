
def test_value_errors(contract_fn: Any) -> None:
    with pytest.raises(ValueError):
        contract_fn("")

    # subscripts must be a string
    with pytest.raises(TypeError):
        contract_fn(0, 0)

    # invalid subscript character
    with pytest.raises(ValueError):
        contract_fn("i%...", [0, 0])
    with pytest.raises(ValueError):
        contract_fn("...j$", [0, 0])
    with pytest.raises(ValueError):
        contract_fn("i->&", [0, 0])

    with pytest.raises(ValueError):
        contract_fn("")
    # number of operands must match count in subscripts string
    with pytest.raises(ValueError):
        contract_fn("", 0, 0)
    with pytest.raises(ValueError):
        contract_fn(",", 0, [0], [0])
    with pytest.raises(ValueError):
        contract_fn(",", [0])

    # can't have more subscripts than dimensions in the operand
    with pytest.raises(ValueError):
        contract_fn("i", 0)
    with pytest.raises(ValueError):
        contract_fn("ij", [0, 0])
    with pytest.raises(ValueError):
        contract_fn("...i", 0)
    with pytest.raises(ValueError):
        contract_fn("i...j", [0, 0])
    with pytest.raises(ValueError):
        contract_fn("i...", 0)
    with pytest.raises(ValueError):
        contract_fn("ij...", [0, 0])

    # invalid ellipsis
    with pytest.raises(ValueError):
        contract_fn("i..", [0, 0])
    with pytest.raises(ValueError):
        contract_fn(".i...", [0, 0])
    with pytest.raises(ValueError):
        contract_fn("j->..j", [0, 0])
    with pytest.raises(ValueError):
        contract_fn("j->.j...", [0, 0])

    # invalid subscript character
    with pytest.raises(ValueError):
        contract_fn("i%...", [0, 0])
    with pytest.raises(ValueError):
        contract_fn("...j$", [0, 0])
    with pytest.raises(ValueError):
        contract_fn("i->&", [0, 0])

    # output subscripts must appear in input
    with pytest.raises(ValueError):
        contract_fn("i->ij", [0, 0])

    # output subscripts may only be specified once
    with pytest.raises(ValueError):
        contract_fn("ij->jij", [[0, 0], [0, 0]])

    # dimensions much match when being collapsed
    with pytest.raises(ValueError):
        contract_fn("ii", np.arange(6).reshape(2, 3))
    with pytest.raises(ValueError):
        contract_fn("ii->i", np.arange(6).reshape(2, 3))

    # broadcasting to new dimensions must be enabled explicitly
    with pytest.raises(ValueError):
        contract_fn("i", np.arange(6).reshape(2, 3))

    with pytest.raises(TypeError):
        contract_fn("ij->ij", [[0, 1], [0, 1]], bad_kwarg=True)

