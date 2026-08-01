
def test_non_final_final():
    with pytest.raises(TypeError) as exc_info:

        class PyNonFinalFinalChild(m.IsNonFinalFinal):
            pass

    assert str(exc_info.value).endswith("is not an acceptable base type")

