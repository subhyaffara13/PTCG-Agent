
def test_bug_correction_tensor_indices():
    # to make sure that tensor_indices does not return a list if creating
    # only one index:
    A = TensorIndexType("A")
    i = tensor_indices('i', A)
    assert not isinstance(i, (tuple, list))
    assert isinstance(i, TensorIndex)

