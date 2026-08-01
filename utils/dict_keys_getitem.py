
def dict_keys_getitem(d: dict[Any, Any], n: int) -> Any:
    # Use dict.keys() to match the iteration order of PyDict_Next used by
    # the C++ DictGuardManager and by ConstDictKeySource._name_template.
    # pyrefly: ignore [bad-argument-type]
    return next(itertools.islice(dict.keys(d), n, n + 1))

