
def test_lacking_copy_ctor():
    with pytest.raises(RuntimeError) as excinfo:
        m.lacking_copy_ctor.get_one()
    assert "is non-copyable!" in str(excinfo.value)

