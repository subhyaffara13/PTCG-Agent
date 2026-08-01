
def filter_seq_schema(*, include: set[int] | None = None, exclude: set[int] | None = None) -> IncExSeqSerSchema:
    return _dict_not_none(type='include-exclude-sequence', include=include, exclude=exclude)

