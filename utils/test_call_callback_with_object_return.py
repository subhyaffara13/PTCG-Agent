
def test_call_callback_with_object_return(call_callback):
    def cb(value):
        if value < 0:
            raise ValueError("Raised from cb")
        return ValueHolder(1000 - value)

    assert call_callback(cb, 287).value == 713

    with pytest.raises(ValueError, match="^Raised from cb$"):
        call_callback(cb, -1)

