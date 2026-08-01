
def test_assert_attr_equal(nulls_fixture):
    obj = SimpleNamespace()
    obj.na_value = nulls_fixture
    tm.assert_attr_equal("na_value", obj, obj)

