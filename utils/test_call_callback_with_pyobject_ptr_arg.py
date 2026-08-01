
def test_call_callback_with_pyobject_ptr_arg():
    def cb(obj):
        return 300 - obj.value

    assert m.call_callback_with_pyobject_ptr_arg(cb, ValueHolder(39)) == 261

