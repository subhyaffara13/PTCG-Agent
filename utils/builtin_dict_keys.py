
def builtin_dict_keys(d: dict[K, V]) -> KeysView[K]:
    # Avoids overridden keys method of the dictionary
    assert isinstance(d, dict)
    return dict.keys(d)

