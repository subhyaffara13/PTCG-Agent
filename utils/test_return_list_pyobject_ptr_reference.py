
def test_return_list_pyobject_ptr_reference():
    vec_obj = m.return_list_pyobject_ptr_reference(ValueHolder)
    assert [e.value for e in vec_obj] == [93, 186]
    # Commenting out the next `assert` will leak the Python references.
    # An easy way to see evidence of the leaks:
    # Insert `while True:` as the first line of this function and monitor the
    # process RES (Resident Memory Size) with the Unix top command.
    assert m.dec_ref_each_pyobject_ptr(vec_obj) == 2

