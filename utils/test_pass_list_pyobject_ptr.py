
def test_pass_list_pyobject_ptr():
    acc = m.pass_list_pyobject_ptr([ValueHolder(842), ValueHolder(452)])
    assert acc == 842452

