
def _filter_usecols(usecols, names: SequenceT) -> SequenceT | list[Hashable]:
    # hackish
    usecols = evaluate_callable_usecols(usecols, names)
    if usecols is not None and len(names) != len(usecols):
        return [name for i, name in enumerate(names) if i in usecols or name in usecols]
    return names

