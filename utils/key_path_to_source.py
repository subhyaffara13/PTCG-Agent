
def key_path_to_source(
    kp: KeyPath, sourced_prefixes: _KeyPathTrie | None = None
) -> Source:
    """
    Given a key path, return the source for the key path.
    """
    if sourced_prefixes is None:
        source: Source = LocalSource("args")
    else:
        source, kp = sourced_prefixes.get(kp)

    for k in kp:
        if isinstance(k, SequenceKey):
            source = GetItemSource(source, k.idx)
        elif isinstance(k, MappingKey):
            source = GetItemSource(source, k.key)
        elif isinstance(k, GetAttrKey):
            source = AttrSource(source, k.name)
        else:
            raise ValueError(f"Unknown KeyEntry {k}")

    return source

