
def _normalize_stix_fontcodes(d: _EntryTypeIn) -> _EntryTypeOut: ...


def _normalize_stix_fontcodes(d: list[_EntryTypeIn]) -> list[_EntryTypeOut]: ...


def _normalize_stix_fontcodes(d: dict[str, list[_EntryTypeIn] |
                                      dict[str, list[_EntryTypeIn]]]
                              ) -> dict[str, list[_EntryTypeOut] |
                                        dict[str, list[_EntryTypeOut]]]: ...


def _normalize_stix_fontcodes(d):
    if isinstance(d, tuple):
        return tuple(ord(x) if isinstance(x, str) and len(x) == 1 else x for x in d)
    elif isinstance(d, list):
        return [_normalize_stix_fontcodes(x) for x in d]
    elif isinstance(d, dict):
        return {k: _normalize_stix_fontcodes(v) for k, v in d.items()}

