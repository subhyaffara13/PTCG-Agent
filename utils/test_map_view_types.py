
def test_map_view_types():
    map_string_double = m.MapStringDouble()
    unordered_map_string_double = m.UnorderedMapStringDouble()
    map_string_double_const = m.MapStringDoubleConst()
    unordered_map_string_double_const = m.UnorderedMapStringDoubleConst()

    assert map_string_double.keys().__class__.__name__ == "KeysView[str]"
    assert map_string_double.values().__class__.__name__ == "ValuesView[float]"
    assert map_string_double.items().__class__.__name__ == "ItemsView[str, float]"

    keys_type = type(map_string_double.keys())
    assert type(unordered_map_string_double.keys()) is keys_type
    assert type(map_string_double_const.keys()) is keys_type
    assert type(unordered_map_string_double_const.keys()) is keys_type

    values_type = type(map_string_double.values())
    assert type(unordered_map_string_double.values()) is values_type
    assert type(map_string_double_const.values()) is values_type
    assert type(unordered_map_string_double_const.values()) is values_type

    items_type = type(map_string_double.items())
    assert type(unordered_map_string_double.items()) is items_type
    assert type(map_string_double_const.items()) is items_type
    assert type(unordered_map_string_double_const.items()) is items_type

