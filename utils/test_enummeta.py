
def test_enummeta():
    from http import HTTPStatus
    import enum
    assert dill.copy(HTTPStatus.OK) is HTTPStatus.OK
    assert dill.copy(enum.EnumMeta) is enum.EnumMeta

