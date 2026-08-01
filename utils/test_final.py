
def test_final():
    with pytest.raises(TypeError) as exc_info:

        class PyFinalChild(m.IsFinal):
            pass

    assert str(exc_info.value).endswith("is not an acceptable base type")

