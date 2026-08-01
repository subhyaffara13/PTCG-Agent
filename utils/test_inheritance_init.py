
def test_inheritance_init(msg):
    # Single base
    class Python(m.Pet):
        def __init__(self):
            pass

    with pytest.raises(TypeError) as exc_info:
        Python()
    expected = "m.class_.Pet.__init__() must be called when overriding __init__"
    assert msg(exc_info.value) == expected

    # Multiple bases
    class RabbitHamster(m.Rabbit, m.Hamster):
        def __init__(self):
            m.Rabbit.__init__(self, "RabbitHamster")

    with pytest.raises(TypeError) as exc_info:
        RabbitHamster()
    expected = "m.class_.Hamster.__init__() must be called when overriding __init__"
    assert msg(exc_info.value) == expected

