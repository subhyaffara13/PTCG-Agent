
def test_owner_is_base(get_module):
    a = get_module.get_array_with_base()
    with pytest.warns(UserWarning, match='warn_on_free'):
        del a
        gc.collect()
        gc.collect()

