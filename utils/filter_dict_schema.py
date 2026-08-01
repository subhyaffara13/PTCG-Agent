
def filter_dict_schema(*, include: IncExDict | None = None, exclude: IncExDict | None = None) -> IncExDictSerSchema:
    return _dict_not_none(type='include-exclude-dict', include=include, exclude=exclude)

