
def test_private_op_new():
    """An object with a private `operator new` cannot be returned by value"""

    with pytest.raises(RuntimeError) as excinfo:
        m.private_op_new_value()
    assert "is neither movable nor copyable" in str(excinfo.value)

    assert m.private_op_new_reference().value == 1

