
def test_return_list_pyobject_ptr_take_ownership():
    vec_obj = m.return_list_pyobject_ptr_take_ownership(ValueHolder)
    assert [e.value for e in vec_obj] == [93, 186]

