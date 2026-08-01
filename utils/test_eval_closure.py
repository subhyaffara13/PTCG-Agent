
def test_eval_closure():
    global_, local = m.test_eval_closure()

    assert global_["closure_value"] == 42
    assert local["closure_value"] == 0

    assert "local_value" not in global_
    assert local["local_value"] == 0

    assert "func_global" not in global_
    assert local["func_global"]() == 42

    assert "func_local" not in global_
    with pytest.raises(NameError):
        local["func_local"]()

