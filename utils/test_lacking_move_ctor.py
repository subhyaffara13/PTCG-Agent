
def test_lacking_move_ctor():
    with pytest.raises(RuntimeError) as excinfo:
        m.lacking_move_ctor.get_one()
    assert "is neither movable nor copyable!" in str(excinfo.value)

