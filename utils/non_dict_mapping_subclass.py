
def non_dict_mapping_subclass() -> type[abc.Mapping]:
    """
    Fixture for a non-mapping dictionary subclass.
    """

    class TestNonDictMapping(abc.Mapping):
        def __init__(self, underlying_dict) -> None:
            self._data = underlying_dict

        def __getitem__(self, key):
            return self._data.__getitem__(key)

        def __iter__(self) -> Iterator:
            return self._data.__iter__()

        def __len__(self) -> int:
            return self._data.__len__()

    return TestNonDictMapping

