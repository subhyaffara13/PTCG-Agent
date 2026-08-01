
def test_smart_ptr_from_default():
    instance = m.HeldByDefaultHolder()
    with pytest.raises(RuntimeError) as excinfo:
        m.HeldByDefaultHolder.load_shared_ptr(instance)
    assert (
        "Unable to load a custom holder type from a "
        "default-holder instance" in str(excinfo.value)
    )

