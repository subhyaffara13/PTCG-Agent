
def test_eval_args():
    # check instance created
    assert isinstance(Density([Ket(0), 0.5], [Ket(1), 0.5]), Density)
    assert isinstance(Density([Qubit('00'), 1/sqrt(2)],
                              [Qubit('11'), 1/sqrt(2)]), Density)

    #test if Qubit object type preserved
    d = Density([Qubit('00'), 1/sqrt(2)], [Qubit('11'), 1/sqrt(2)])
    for (state, prob) in d.args:
        assert isinstance(state, Qubit)

    # check for value error, when prob is not provided
    raises(ValueError, lambda: Density([Ket(0)], [Ket(1)]))

