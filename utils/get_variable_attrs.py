
def getVariableAttrs(cls: BaseTable, fmt: Optional[int] = None) -> Tuple[str]:
    """Return sequence of variable table field names (can be empty).

    Attributes are deemed "variable" when their otData.py's description contain
    'VarIndexBase + {offset}', e.g. COLRv1 PaintVar* tables.
    """
    if not issubclass(cls, BaseTable):
        raise TypeError(cls)
    if issubclass(cls, FormatSwitchingBaseTable):
        if fmt is None:
            raise TypeError(f"'fmt' is required for format-switching {cls.__name__}")
        converters = cls.convertersByName[fmt]
    else:
        converters = cls.convertersByName
    # assume if no 'VarIndexBase' field is present, table has no variable fields
    if "VarIndexBase" not in converters:
        return ()
    varAttrs = {}
    for name, conv in converters.items():
        offset = conv.getVarIndexOffset()
        if offset is not None:
            varAttrs[name] = offset
    return tuple(sorted(varAttrs, key=varAttrs.__getitem__))

