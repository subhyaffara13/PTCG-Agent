
def getitem_on_dict_manager(
    source: DictGetItemSource | DictSubclassGetItemSource,
    base_guard_manager: DictGuardManager,
    base_example_value: Any,
    example_value: Any,
    guard_manager_enum: GuardManagerType,
) -> GuardManager:
    base_source_name = source.base.name
    if isinstance(source.index, ConstDictKeySource):
        index = source.index.index
    else:
        assert isinstance(base_example_value, dict)
        index = get_key_index(base_example_value, source.index)

    key_source = get_key_index_source(base_source_name, index)

    # Ensure that we call dict.keys and not value.keys (which can call
    # overridden keys method). In the C++ guards, we relied on PyDict_Next
    # to traverse the dictionary, which uses the internal data structure and
    # does not call the overridden keys method.
    key_example_value = list(builtin_dict_keys(base_example_value))[index]
    if isinstance(key_example_value, (int, str)):
        value_source = f"{base_source_name}[{key_example_value!r}]"
    else:
        value_source = f"{base_source_name}[{key_source}]"
    if not isinstance(source.index, ConstDictKeySource):
        # We have to insert a key manager guard here
        # TODO - source debug string is probably wrong here.
        base_guard_manager.get_key_manager(
            index=index,
            source=key_source,
            example_value=source.index,
            guard_manager_enum=GuardManagerType.GUARD_MANAGER,
        ).add_equals_match_guard(
            source.index, [f"{key_source} == {key_example_value!r}"], None
        )

    return base_guard_manager.get_value_manager(
        index=index,
        source=value_source,
        example_value=example_value,
        guard_manager_enum=guard_manager_enum,
    )

