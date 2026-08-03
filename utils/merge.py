import copy

def merge(arg, default, override, args, kwargs):
    '''Merge all the possible arguments into a tuple and a dictionary.

    :param arg: The argument's name.
    :param default: The argument's default value or an instance of _POSITIONAL.
    :param override: A tuple containing (args, kwargs) given to @arg.
    :param args: The arguments extracted from the docstring.
    :param kwargs: The keyword arguments extracted from the docstring.'''
    opts = [arg]
    if not isinstance(default, _POSITIONAL):
        opts = list(ensure_dashes(args or opts))
        kwargs.update({'default': default, 'dest': arg})
        kwargs.update(action_by_type(default))
    else:
        # positionals can't have a metavar, otherwise the help is screwed
        # if one really wants the metavar, it can be added with @arg
        kwargs['metavar'] = None
    kwargs.update(override[1])
    return override[0] or opts, kwargs


def merge(seqs: list[list[TypeInfo]]) -> list[TypeInfo]:
    seqs = [s.copy() for s in seqs]
    result: list[TypeInfo] = []
    while True:
        seqs = [s for s in seqs if s]
        if not seqs:
            return result
        for seq in seqs:
            head = seq[0]
            if not [s for s in seqs if head in s[1:]]:
                break
        else:
            raise MroError()
        result.append(head)
        for s in seqs:
            if s[0] is head:
                del s[0]


def merge(mode: str, bands: Sequence[Image]) -> Image:
    """
    Merge a set of single band images into a new multiband image.

    :param mode: The mode to use for the output image. See:
        :ref:`concept-modes`.
    :param bands: A sequence containing one single-band image for
        each band in the output image.  All bands must have the
        same size.
    :returns: An :py:class:`~PIL.Image.Image` object.
    """

    if getmodebands(mode) != len(bands) or "*" in mode:
        msg = "wrong number of bands"
        raise ValueError(msg)
    for band in bands[1:]:
        if band.mode != getmodetype(mode):
            msg = "mode mismatch"
            raise ValueError(msg)
        if band.size != bands[0].size:
            msg = "size mismatch"
            raise ValueError(msg)
    for band in bands:
        band.load()
    return bands[0]._new(core.merge(mode, *[b.im for b in bands]))


def merge(*dicts, **kwargs):
    """ Merge a collection of dictionaries

    >>> merge({1: 'one'}, {2: 'two'})
    {1: 'one', 2: 'two'}

    Later dictionaries have precedence

    >>> merge({1: 2, 3: 4}, {3: 3, 4: 4})
    {1: 2, 3: 3, 4: 4}

    See Also:
        merge_with
    """
    if len(dicts) == 1 and not isinstance(dicts[0], Mapping):
        dicts = dicts[0]
    factory = _get_factory(merge, kwargs)

    rv = factory()
    for d in dicts:
        rv.update(d)
    return rv


def merge(*iterables, key=None, reverse=False):  # type: ignore[no-untyped-def]
    return py_heapq.merge(*iterables, key=key, reverse=reverse)


def merge(*dicts, **kwargs):
    """Merge a collection of dictionaries

    >>> merge({1: "one"}, {2: "two"})
    {1: 'one', 2: 'two'}

    Later dictionaries have precedence

    >>> merge({1: 2, 3: 4}, {3: 3, 4: 4})
    {1: 2, 3: 3, 4: 4}

    See Also:
        merge_with
    """
    if len(dicts) == 1 and not isinstance(dicts[0], Mapping):
        dicts = dicts[0]
    factory = _get_factory(merge, kwargs)

    rv = factory()
    for d in dicts:
        rv.update(d)
    return rv


def merge(d, *dicts, **kwargs):
    return toolz.merge(d, *dicts, **kwargs)


def merge(
    left: DataFrame | Series,
    right: DataFrame | Series,
    how: MergeHow = "inner",
    on: IndexLabel | AnyArrayLike | None = None,
    left_on: IndexLabel | AnyArrayLike | None = None,
    right_on: IndexLabel | AnyArrayLike | None = None,
    left_index: bool = False,
    right_index: bool = False,
    sort: bool = False,
    suffixes: Suffixes = ("_x", "_y"),
    copy: bool | lib.NoDefault = lib.no_default,
    indicator: str | bool = False,
    validate: str | None = None,
) -> DataFrame:
    """
    Merge DataFrame or named Series objects with a database-style join.

    A named Series object is treated as a DataFrame with a single named column.

    The join is done on columns or indexes. If joining columns on
    columns, the DataFrame indexes *will be ignored*. Otherwise if joining indexes
    on indexes or indexes on a column or columns, the index will be passed on.
    When performing a cross merge, no column specifications to merge on are
    allowed.

    .. warning::

        If both key columns contain rows where the key is a null value, those
        rows will be matched against each other. This is different from usual SQL
        join behaviour and can lead to unexpected results.

    Parameters
    ----------
    left : DataFrame or named Series
        First pandas object to merge.
    right : DataFrame or named Series
        Second pandas object to merge.
    how : {'left', 'right', 'outer', 'inner', 'cross', 'left_anti', 'right_anti},
        default 'inner'
        Type of merge to be performed.

        * left: use only keys from left frame, similar to a SQL left outer join;
          preserve key order.
        * right: use only keys from right frame, similar to a SQL right outer join;
          preserve key order.
        * outer: use union of keys from both frames, similar to a SQL full outer
          join; sort keys lexicographically.
        * inner: use intersection of keys from both frames, similar to a SQL inner
          join; preserve the order of the left keys.
        * cross: creates the cartesian product from both frames, preserves the order
          of the left keys.
        * left_anti: use only keys from left frame that are not in right frame, similar
          to SQL left anti join; preserve key order.
        * right_anti: use only keys from right frame that are not in left frame, similar
          to SQL right anti join; preserve key order.
    on : Hashable or a sequence of the previous
        Column or index level names to join on. These must be found in both
        DataFrames. If `on` is None and not merging on indexes then this defaults
        to the intersection of the columns in both DataFrames.
    left_on : Hashable or a sequence of the previous, or array-like
        Column or index level names to join on in the left DataFrame. Can also
        be an array or list of arrays of the length of the left DataFrame.
        These arrays are treated as if they are columns.
    right_on : Hashable or a sequence of the previous, or array-like
        Column or index level names to join on in the right DataFrame. Can also
        be an array or list of arrays of the length of the right DataFrame.
        These arrays are treated as if they are columns.
    left_index : bool, default False
        Use the index from the left DataFrame as the join key(s). If it is a
        MultiIndex, the number of keys in the other DataFrame (either the index
        or a number of columns) must match the number of levels.
    right_index : bool, default False
        Use the index from the right DataFrame as the join key. Same caveats as
        left_index.
    sort : bool, default False
        Sort the join keys lexicographically in the result DataFrame. If False,
        the order of the join keys depends on the join type (how keyword).
    suffixes : list-like, default is ("_x", "_y")
        A length-2 sequence where each element is optionally a string
        indicating the suffix to add to overlapping column names in
        `left` and `right` respectively. Pass a value of `None` instead
        of a string to indicate that the column name from `left` or
        `right` should be left as-is, with no suffix. At least one of the
        values must not be None.
    copy : bool, default False
        This keyword is now ignored; changing its value will have no
        impact on the method.

        .. deprecated:: 3.0.0

            This keyword is ignored and will be removed in pandas 4.0. Since
            pandas 3.0, this method always returns a new object using a lazy
            copy mechanism that defers copies until necessary
            (Copy-on-Write). See the `user guide on Copy-on-Write
            <https://pandas.pydata.org/docs/dev/user_guide/copy_on_write.html>`__
            for more details.

    indicator : bool or str, default False
        If True, adds a column to the output DataFrame called "_merge" with
        information on the source of each row. The column can be given a different
        name by providing a string argument. The column will have a Categorical
        type with the value of "left_only" for observations whose merge key only
        appears in the left DataFrame, "right_only" for observations
        whose merge key only appears in the right DataFrame, and "both"
        if the observation's merge key is found in both DataFrames.

    validate : str, optional
        If specified, checks if merge is of specified type.

        * "one_to_one" or "1:1": check if merge keys are unique in both
          left and right datasets.
        * "one_to_many" or "1:m": check if merge keys are unique in left
          dataset.
        * "many_to_one" or "m:1": check if merge keys are unique in right
          dataset.
        * "many_to_many" or "m:m": allowed, but does not result in checks.

    Returns
    -------
    DataFrame
        A DataFrame of the two merged objects.

    See Also
    --------
    merge_ordered : Merge with optional filling/interpolation.
    merge_asof : Merge on nearest keys.
    DataFrame.join : Similar method using indices.

    Examples
    --------
    >>> df1 = pd.DataFrame(
    ...     {"lkey": ["foo", "bar", "baz", "foo"], "value": [1, 2, 3, 5]}
    ... )
    >>> df2 = pd.DataFrame(
    ...     {"rkey": ["foo", "bar", "baz", "foo"], "value": [5, 6, 7, 8]}
    ... )
    >>> df1
        lkey value
    0   foo      1
    1   bar      2
    2   baz      3
    3   foo      5
    >>> df2
        rkey value
    0   foo      5
    1   bar      6
    2   baz      7
    3   foo      8

    Merge df1 and df2 on the lkey and rkey columns. The value columns have
    the default suffixes, _x and _y, appended.

    >>> df1.merge(df2, left_on="lkey", right_on="rkey")
      lkey  value_x rkey  value_y
    0  foo        1  foo        5
    1  foo        1  foo        8
    2  bar        2  bar        6
    3  baz        3  baz        7
    4  foo        5  foo        5
    5  foo        5  foo        8

    Merge DataFrames df1 and df2 with specified left and right suffixes
    appended to any overlapping columns.

    >>> df1.merge(df2, left_on="lkey", right_on="rkey", suffixes=("_left", "_right"))
      lkey  value_left rkey  value_right
    0  foo           1  foo            5
    1  foo           1  foo            8
    2  bar           2  bar            6
    3  baz           3  baz            7
    4  foo           5  foo            5
    5  foo           5  foo            8

    Merge DataFrames df1 and df2, but raise an exception if the DataFrames have
    any overlapping columns.

    >>> df1.merge(df2, left_on="lkey", right_on="rkey", suffixes=(False, False))
    Traceback (most recent call last):
    ...
    ValueError: columns overlap but no suffix specified:
        Index(['value'], dtype='str')

    >>> df1 = pd.DataFrame({"a": ["foo", "bar"], "b": [1, 2]})
    >>> df2 = pd.DataFrame({"a": ["foo", "baz"], "c": [3, 4]})
    >>> df1
          a  b
    0   foo  1
    1   bar  2
    >>> df2
          a  c
    0   foo  3
    1   baz  4

    >>> df1.merge(df2, how="inner", on="a")
          a  b  c
    0   foo  1  3

    >>> df1.merge(df2, how="left", on="a")
          a  b  c
    0   foo  1  3.0
    1   bar  2  NaN

    >>> df1 = pd.DataFrame({"left": ["foo", "bar"]})
    >>> df2 = pd.DataFrame({"right": [7, 8]})
    >>> df1
        left
    0   foo
    1   bar
    >>> df2
        right
    0   7
    1   8

    >>> df1.merge(df2, how="cross")
       left  right
    0   foo      7
    1   foo      8
    2   bar      7
    3   bar      8
    """
    left_df = _validate_operand(left)
    left._check_copy_deprecation(copy)
    right_df = _validate_operand(right)
    if how == "cross":
        return _cross_merge(
            left_df,
            right_df,
            on=on,
            left_on=left_on,
            right_on=right_on,
            left_index=left_index,
            right_index=right_index,
            sort=sort,
            suffixes=suffixes,
            indicator=indicator,
            validate=validate,
        )
    else:
        op = _MergeOperation(
            left_df,
            right_df,
            how=how,
            on=on,
            left_on=left_on,
            right_on=right_on,
            left_index=left_index,
            right_index=right_index,
            sort=sort,
            suffixes=suffixes,
            indicator=indicator,
            validate=validate,
        )
        return op.get_result()


def Merge(text,
          message,
          allow_unknown_extension=False,
          allow_field_number=False,
          descriptor_pool=None,
          allow_unknown_field=False,
          max_recursion_depth=None):
  """Parses a text representation of a protocol message into a message.

  Like Parse(), but allows repeated values for a non-repeated field, and uses
  the last one. This means any non-repeated, top-level fields specified in text
  replace those in the message.

  Args:
    text (str): Message text representation.
    message (Message): A protocol buffer message to merge into.
    allow_unknown_extension: if True, skip over missing extensions and keep
      parsing
    allow_field_number: if True, both field number and field name are allowed.
    descriptor_pool (DescriptorPool): Descriptor pool used to resolve Any types.
    allow_unknown_field: if True, skip over unknown field and keep
      parsing. Avoid to use this option if possible. It may hide some
      errors (e.g. spelling error on field name)
    max_recursion_depth: Optional maximum recursion depth of a text proto
      message to be deserialized. Text proto messages over this depth will
      fail to parse. ``None`` keeps the historical unbounded behavior.

  Returns:
    Message: The same message passed as argument.

  Raises:
    ParseError: On text parsing problems.
  """
  return MergeLines(
      text.split(b'\n' if isinstance(text, bytes) else u'\n'),
      message,
      allow_unknown_extension,
      allow_field_number,
      descriptor_pool=descriptor_pool,
      allow_unknown_field=allow_unknown_field,
      max_recursion_depth=max_recursion_depth)


def merge(self, m, tables):
    if not hasattr(self, "mergeMap"):
        log.info("Don't know how to merge '%s'.", self.tableTag)
        return NotImplemented

    logic = self.mergeMap

    if isinstance(logic, dict):
        return m.mergeObjects(self, self.mergeMap, tables)
    else:
        return logic(tables)


def merge(self, m, tables):
    assert len(tables) == len(m.duplicateGlyphsPerFont)
    for i, (table, dups) in enumerate(zip(tables, m.duplicateGlyphsPerFont)):
        if not dups:
            continue
        if table is None or table is NotImplemented:
            log.warning(
                "Have non-identical duplicates to resolve for '%s' but no GSUB. Are duplicates intended?: %s",
                m.fonts[i]._merger__name,
                dups,
            )
            continue

        synthFeature = None
        synthLookup = None
        for script in table.table.ScriptList.ScriptRecord:
            if script.ScriptTag == "DFLT":
                continue  # XXX
            for langsys in [script.Script.DefaultLangSys] + [
                l.LangSys for l in script.Script.LangSysRecord
            ]:
                if langsys is None:
                    continue  # XXX Create!
                feature = [v for v in langsys.FeatureIndex if v.FeatureTag == "locl"]
                assert len(feature) <= 1
                if feature:
                    feature = feature[0]
                else:
                    if not synthFeature:
                        synthFeature = otTables.FeatureRecord()
                        synthFeature.FeatureTag = "locl"
                        f = synthFeature.Feature = otTables.Feature()
                        f.FeatureParams = None
                        f.LookupCount = 0
                        f.LookupListIndex = []
                        table.table.FeatureList.FeatureRecord.append(synthFeature)
                        table.table.FeatureList.FeatureCount += 1
                    feature = synthFeature
                    langsys.FeatureIndex.append(feature)
                    langsys.FeatureIndex.sort(key=lambda v: v.FeatureTag)

                if not synthLookup:
                    subtable = otTables.SingleSubst()
                    subtable.mapping = dups
                    synthLookup = otTables.Lookup()
                    synthLookup.LookupFlag = 0
                    synthLookup.LookupType = 1
                    synthLookup.SubTableCount = 1
                    synthLookup.SubTable = [subtable]
                    if table.table.LookupList is None:
                        # mtiLib uses None as default value for LookupList,
                        # while feaLib points to an empty array with count 0
                        # TODO: make them do the same
                        table.table.LookupList = otTables.LookupList()
                        table.table.LookupList.Lookup = []
                        table.table.LookupList.LookupCount = 0
                    table.table.LookupList.Lookup.append(synthLookup)
                    table.table.LookupList.LookupCount += 1

                if feature.Feature.LookupListIndex[:1] != [synthLookup]:
                    feature.Feature.LookupListIndex[:0] = [synthLookup]
                    feature.Feature.LookupCount += 1

    DefaultTable.merge(self, m, tables)
    return self


def merge(self, m, tables):
    DefaultTable.merge(self, m, tables)
    if self.version < 2:
        # bits 8 and 9 are reserved and should be set to zero
        self.fsType &= ~0x0300
    if self.version >= 3:
        # Only one of bits 1, 2, and 3 may be set. We already take
        # care of bit 1 implications in mergeOs2FsType. So unset
        # bit 2 if bit 3 is already set.
        if self.fsType & 0x0008:
            self.fsType &= ~0x0004
    return self


def merge(self, m, tables):
    for i, table in enumerate(tables):
        for g in table.glyphs.values():
            if i:
                # Drop hints for all but first font, since
                # we don't map functions / CVT values.
                g.removeHinting()
            # Expand composite glyphs to load their
            # composite glyph names.
            if g.isComposite():
                g.expand(table)
    return DefaultTable.merge(self, m, tables)


def merge(self, m, tables):
    if any(hasattr(table.cff[0], "FDSelect") for table in tables):
        raise NotImplementedError("Merging CID-keyed CFF tables is not supported yet")

    for table in tables:
        table.cff.desubroutinize()

    newcff = tables[0]
    newfont = newcff.cff[0]
    private = newfont.Private
    newDefaultWidthX, newNominalWidthX = private.defaultWidthX, private.nominalWidthX
    storedNamesStrings = []
    glyphOrderStrings = []
    glyphOrder = set(newfont.getGlyphOrder())

    for name in newfont.strings.strings:
        if name not in glyphOrder:
            storedNamesStrings.append(name)
        else:
            glyphOrderStrings.append(name)

    chrset = list(newfont.charset)
    newcs = newfont.CharStrings
    log.debug("FONT 0 CharStrings: %d.", len(newcs))

    for i, table in enumerate(tables[1:], start=1):
        font = table.cff[0]
        defaultWidthX, nominalWidthX = (
            font.Private.defaultWidthX,
            font.Private.nominalWidthX,
        )
        widthsDiffer = (
            defaultWidthX != newDefaultWidthX or nominalWidthX != newNominalWidthX
        )
        font.Private = private
        fontGlyphOrder = set(font.getGlyphOrder())
        for name in font.strings.strings:
            if name in fontGlyphOrder:
                glyphOrderStrings.append(name)
        cs = font.CharStrings
        gs = table.cff.GlobalSubrs
        log.debug("Font %d CharStrings: %d.", i, len(cs))
        chrset.extend(font.charset)
        if newcs.charStringsAreIndexed:
            for i, name in enumerate(cs.charStrings, start=len(newcs)):
                newcs.charStrings[name] = i
                newcs.charStringsIndex.items.append(None)
        for name in cs.charStrings:
            if widthsDiffer:
                c = cs[name]
                defaultWidthXToken = object()
                extractor = T2WidthExtractor([], [], nominalWidthX, defaultWidthXToken)
                extractor.execute(c)
                width = extractor.width
                if width is not defaultWidthXToken:
                    # The following will be wrong if the width is added
                    # by a subroutine. Ouch!
                    c.program.pop(0)
                else:
                    width = defaultWidthX
                if width != newDefaultWidthX:
                    c.program.insert(0, width - newNominalWidthX)
            newcs[name] = cs[name]

    newfont.charset = chrset
    newfont.numGlyphs = len(chrset)
    newfont.strings.strings = glyphOrderStrings + storedNamesStrings

    return newcff


def merge(self, m, tables):
    if not hasattr(m, "cmap"):
        computeMegaCmap(m, tables)
    cmap = m.cmap

    cmapBmpOnly = {uni: gid for uni, gid in cmap.items() if uni <= 0xFFFF}
    self.tables = []
    module = ttLib.getTableModule("cmap")
    if len(cmapBmpOnly) != len(cmap):
        # format-12 required.
        cmapTable = module.cmap_classes[12](12)
        cmapTable.platformID = 3
        cmapTable.platEncID = 10
        cmapTable.language = 0
        cmapTable.cmap = cmap
        self.tables.append(cmapTable)
    # always create format-4
    cmapTable = module.cmap_classes[4](4)
    cmapTable.platformID = 3
    cmapTable.platEncID = 1
    cmapTable.language = 0
    cmapTable.cmap = cmapBmpOnly
    # ordered by platform then encoding
    self.tables.insert(0, cmapTable)

    uvsDict = m.uvsDict
    if uvsDict:
        # format-14
        uvsTable = module.cmap_classes[14](14)
        uvsTable.platformID = 0
        uvsTable.platEncID = 5
        uvsTable.language = 0
        uvsTable.cmap = {}
        uvsTable.uvsDict = uvsDict
        # ordered by platform then encoding
        self.tables.insert(0, uvsTable)
    self.tableVersion = 0
    self.numSubTables = len(self.tables)
    return self


def merge(merger, self, lst):
    if self is None:
        if not allNone(lst):
            raise NotANone(merger, expected=None, got=lst)
        return

    lst = [l.classDefs for l in lst]
    self.classDefs = {}
    # We only care about the .classDefs
    self = self.classDefs

    allKeys = set()
    allKeys.update(*[l.keys() for l in lst])
    for k in allKeys:
        allValues = nonNone(l.get(k) for l in lst)
        if not allEqual(allValues):
            raise ShouldBeConstant(
                merger, expected=allValues[0], got=lst, stack=["." + k]
            )
        if not allValues:
            self[k] = None
        else:
            self[k] = allValues[0]


def merge(merger, self, lst):
    # Code below sometimes calls us with self being
    # a new object. Copy it from lst and recurse.
    self.__dict__ = lst[0].__dict__.copy()
    merger.mergeObjects(self, lst)


def merge(merger, self, lst):
    # Code below sometimes calls us with self being
    # a new object. Copy it from lst and recurse.
    self.__dict__ = lst[0].__dict__.copy()
    merger.mergeObjects(self, lst)


def merge(merger, self, lst):
    self.ValueFormat = valueFormat = reduce(int.__or__, [l.ValueFormat for l in lst], 0)
    if not (len(lst) == 1 or (valueFormat & ~0xF == 0)):
        raise UnsupportedFormat(merger, subtable="single positioning lookup")

    # If all have same coverage table and all are format 1,
    coverageGlyphs = self.Coverage.glyphs
    if all(v.Format == 1 for v in lst) and all(
        coverageGlyphs == v.Coverage.glyphs for v in lst
    ):
        self.Value = otBase.ValueRecord(valueFormat, self.Value)
        if valueFormat != 0:
            # If v.Value is None, it means a kerning of 0; we want
            # it to participate in the model still.
            # https://github.com/fonttools/fonttools/issues/3111
            merger.mergeThings(
                self.Value,
                [v.Value if v.Value is not None else otBase.ValueRecord() for v in lst],
            )
        self.ValueFormat = self.Value.getFormat()
        return

    # Upgrade everything to Format=2
    self.Format = 2
    lst = [_SinglePosUpgradeToFormat2(v) for v in lst]

    # Align them
    glyphs, padded = _merge_GlyphOrders(
        merger.font, [v.Coverage.glyphs for v in lst], [v.Value for v in lst]
    )

    self.Coverage.glyphs = glyphs
    self.Value = [otBase.ValueRecord(valueFormat) for _ in glyphs]
    self.ValueCount = len(self.Value)

    for i, values in enumerate(padded):
        for j, glyph in enumerate(glyphs):
            if values[j] is not None:
                continue
            # Fill in value from other subtables
            # Note!!! This *might* result in behavior change if ValueFormat2-zeroedness
            # is different between used subtable and current subtable!
            # TODO(behdad) Check and warn if that happens?
            v = _Lookup_SinglePos_get_effective_value(
                merger, merger.lookup_subtables[i], glyph
            )
            if v is None:
                v = otBase.ValueRecord(valueFormat)
            values[j] = v

    merger.mergeLists(self.Value, padded)

    # Merge everything else; though, there shouldn't be anything else. :)
    merger.mergeObjects(
        self, lst, exclude=("Format", "Coverage", "Value", "ValueCount", "ValueFormat")
    )
    self.ValueFormat = reduce(
        int.__or__, [v.getEffectiveFormat() for v in self.Value], 0
    )


def merge(merger, self, lst):
    # Align them
    glyphs, padded = _merge_GlyphOrders(
        merger.font,
        [[v.SecondGlyph for v in vs.PairValueRecord] for vs in lst],
        [vs.PairValueRecord for vs in lst],
    )

    self.PairValueRecord = pvrs = []
    for glyph in glyphs:
        pvr = ot.PairValueRecord()
        pvr.SecondGlyph = glyph
        pvr.Value1 = (
            otBase.ValueRecord(merger.valueFormat1) if merger.valueFormat1 else None
        )
        pvr.Value2 = (
            otBase.ValueRecord(merger.valueFormat2) if merger.valueFormat2 else None
        )
        pvrs.append(pvr)
    self.PairValueCount = len(self.PairValueRecord)

    for i, values in enumerate(padded):
        for j, glyph in enumerate(glyphs):
            # Fill in value from other subtables
            v = ot.PairValueRecord()
            v.SecondGlyph = glyph
            if values[j] is not None:
                vpair = values[j]
            else:
                vpair = _Lookup_PairPos_get_effective_value_pair(
                    merger, merger.lookup_subtables[i], self._firstGlyph, glyph
                )
            if vpair is None:
                v1, v2 = None, None
            else:
                v1 = getattr(vpair, "Value1", None)
                v2 = getattr(vpair, "Value2", None)
            v.Value1 = (
                otBase.ValueRecord(merger.valueFormat1, src=v1)
                if merger.valueFormat1
                else None
            )
            v.Value2 = (
                otBase.ValueRecord(merger.valueFormat2, src=v2)
                if merger.valueFormat2
                else None
            )
            values[j] = v
    del self._firstGlyph

    merger.mergeLists(self.PairValueRecord, padded)


def merge(merger, self, lst):
    merger.valueFormat1 = self.ValueFormat1 = reduce(
        int.__or__, [l.ValueFormat1 for l in lst], 0
    )
    merger.valueFormat2 = self.ValueFormat2 = reduce(
        int.__or__, [l.ValueFormat2 for l in lst], 0
    )

    if self.Format == 1:
        _PairPosFormat1_merge(self, lst, merger)
    elif self.Format == 2:
        _PairPosFormat2_merge(self, lst, merger)
    else:
        raise UnsupportedFormat(merger, subtable="pair positioning lookup")

    del merger.valueFormat1, merger.valueFormat2

    # Now examine the list of value records, and update to the union of format values,
    # as merge might have created new values.
    vf1 = 0
    vf2 = 0
    if self.Format == 1:
        for pairSet in self.PairSet:
            for pairValueRecord in pairSet.PairValueRecord:
                pv1 = getattr(pairValueRecord, "Value1", None)
                if pv1 is not None:
                    vf1 |= pv1.getFormat()
                pv2 = getattr(pairValueRecord, "Value2", None)
                if pv2 is not None:
                    vf2 |= pv2.getFormat()
    elif self.Format == 2:
        for class1Record in self.Class1Record:
            for class2Record in class1Record.Class2Record:
                pv1 = getattr(class2Record, "Value1", None)
                if pv1 is not None:
                    vf1 |= pv1.getFormat()
                pv2 = getattr(class2Record, "Value2", None)
                if pv2 is not None:
                    vf2 |= pv2.getFormat()
    self.ValueFormat1 = vf1
    self.ValueFormat2 = vf2


def merge(merger, self, lst):
    if not allEqualTo(self.Format, (l.Format for l in lst)):
        raise InconsistentFormats(
            merger,
            subtable="mark-to-base positioning lookup",
            expected=self.Format,
            got=[l.Format for l in lst],
        )
    if self.Format == 1:
        _MarkBasePosFormat1_merge(self, lst, merger)
    else:
        raise UnsupportedFormat(merger, subtable="mark-to-base positioning lookup")


def merge(merger, self, lst):
    if not allEqualTo(self.Format, (l.Format for l in lst)):
        raise InconsistentFormats(
            merger,
            subtable="mark-to-mark positioning lookup",
            expected=self.Format,
            got=[l.Format for l in lst],
        )
    if self.Format == 1:
        _MarkBasePosFormat1_merge(self, lst, merger, "Mark1", "Mark2")
    else:
        raise UnsupportedFormat(merger, subtable="mark-to-mark positioning lookup")


def merge(merger, self, lst):
    # Align them
    glyphs, padded = _merge_GlyphOrders(
        merger.font,
        [l.Coverage.glyphs for l in lst],
        [l.EntryExitRecord for l in lst],
    )

    self.Format = 1
    self.Coverage = ot.Coverage()
    self.Coverage.glyphs = glyphs
    self.EntryExitRecord = []
    for _ in glyphs:
        rec = ot.EntryExitRecord()
        rec.EntryAnchor = ot.Anchor()
        rec.EntryAnchor.Format = 1
        rec.ExitAnchor = ot.Anchor()
        rec.ExitAnchor.Format = 1
        self.EntryExitRecord.append(rec)
    merger.mergeLists(self.EntryExitRecord, padded)
    self.EntryExitCount = len(self.EntryExitRecord)


def merge(merger, self, lst):
    if all(master.EntryAnchor is None for master in lst):
        self.EntryAnchor = None
    if all(master.ExitAnchor is None for master in lst):
        self.ExitAnchor = None
    merger.mergeObjects(self, lst)


def merge(merger, self, lst):
    subtables = merger.lookup_subtables = [l.SubTable for l in lst]

    # Remove Extension subtables
    for l, sts in list(zip(lst, subtables)) + [(self, self.SubTable)]:
        if not sts:
            continue
        if sts[0].__class__.__name__.startswith("Extension"):
            if not allEqual([st.__class__ for st in sts]):
                raise InconsistentExtensions(
                    merger,
                    expected="Extension",
                    got=[st.__class__.__name__ for st in sts],
                )
            if not allEqual([st.ExtensionLookupType for st in sts]):
                raise InconsistentExtensions(merger)
            l.LookupType = sts[0].ExtensionLookupType
            new_sts = [st.ExtSubTable for st in sts]
            del sts[:]
            sts.extend(new_sts)

    isPairPos = self.SubTable and isinstance(self.SubTable[0], ot.PairPos)

    if isPairPos:
        # AFDKO and feaLib sometimes generate two Format1 subtables instead of one.
        # Merge those before continuing.
        # https://github.com/fonttools/fonttools/issues/719
        self.SubTable = _Lookup_PairPos_subtables_canonicalize(
            self.SubTable, merger.font
        )
        subtables = merger.lookup_subtables = [
            _Lookup_PairPos_subtables_canonicalize(st, merger.font) for st in subtables
        ]
    else:
        isSinglePos = self.SubTable and isinstance(self.SubTable[0], ot.SinglePos)
        if isSinglePos:
            numSubtables = [len(st) for st in subtables]
            if not all([nums == numSubtables[0] for nums in numSubtables]):
                # Flatten list of SinglePos subtables to single Format 2 subtable,
                # with all value records set to the rec format type.
                # We use buildSinglePos() to optimize the lookup after merging.
                valueFormatList = [t.ValueFormat for st in subtables for t in st]
                # Find the minimum value record that can accomodate all the singlePos subtables.
                mirf = reduce(ior, valueFormatList)
                self.SubTable = _Lookup_SinglePos_subtables_flatten(
                    self.SubTable, merger.font, mirf
                )
                subtables = merger.lookup_subtables = [
                    _Lookup_SinglePos_subtables_flatten(st, merger.font, mirf)
                    for st in subtables
                ]
                flattened = True
            else:
                flattened = False

    merger.mergeLists(self.SubTable, subtables)
    self.SubTableCount = len(self.SubTable)

    if isPairPos:
        # If format-1 subtable created during canonicalization is empty, remove it.
        assert len(self.SubTable) >= 1 and self.SubTable[0].Format == 1
        if not self.SubTable[0].Coverage.glyphs:
            self.SubTable.pop(0)
            self.SubTableCount -= 1

        # If format-2 subtable created during canonicalization is empty, remove it.
        assert len(self.SubTable) >= 1 and self.SubTable[-1].Format == 2
        if not self.SubTable[-1].Coverage.glyphs:
            self.SubTable.pop(-1)
            self.SubTableCount -= 1

        # Compact the merged subtables
        # This is a good moment to do it because the compaction should create
        # smaller subtables, which may prevent overflows from happening.
        # Keep reading the value from the ENV until ufo2ft switches to the config system
        level = merger.font.cfg.get(
            "fontTools.otlLib.optimize.gpos:COMPRESSION_LEVEL",
            default=_compression_level_from_env(),
        )
        if level != 0:
            log.info("Compacting GPOS...")
            self.SubTable = compact_pair_pos(merger.font, level, self.SubTable)
            self.SubTableCount = len(self.SubTable)

    elif isSinglePos and flattened:
        singlePosTable = self.SubTable[0]
        glyphs = singlePosTable.Coverage.glyphs
        # We know that singlePosTable is Format 2, as this is set
        # in _Lookup_SinglePos_subtables_flatten.
        singlePosMapping = {
            gname: valRecord for gname, valRecord in zip(glyphs, singlePosTable.Value)
        }
        self.SubTable = buildSinglePos(
            singlePosMapping, merger.font.getReverseGlyphMap()
        )
    merger.mergeObjects(self, lst, exclude=["SubTable", "SubTableCount"])

    del merger.lookup_subtables


def merge(merger, self, lst):
    assert self.Format == 1
    Coords = [a.Coordinate for a in lst]
    model = merger.model
    masterScalars = merger.masterScalars
    self.Coordinate = otRound(
        model.interpolateFromValuesAndScalars(Coords, masterScalars)
    )


def merge(merger, self, lst):
    assert self.Format == 1
    XCoords = [a.XCoordinate for a in lst]
    YCoords = [a.YCoordinate for a in lst]
    model = merger.model
    masterScalars = merger.masterScalars
    self.XCoordinate = otRound(
        model.interpolateFromValuesAndScalars(XCoords, masterScalars)
    )
    self.YCoordinate = otRound(
        model.interpolateFromValuesAndScalars(YCoords, masterScalars)
    )


def merge(merger, self, lst):
    model = merger.model
    masterScalars = merger.masterScalars
    # TODO Handle differing valueformats
    for name, tableName in [
        ("XAdvance", "XAdvDevice"),
        ("YAdvance", "YAdvDevice"),
        ("XPlacement", "XPlaDevice"),
        ("YPlacement", "YPlaDevice"),
    ]:
        assert not hasattr(self, tableName)

        if hasattr(self, name):
            values = [getattr(a, name, 0) for a in lst]
            value = otRound(
                model.interpolateFromValuesAndScalars(values, masterScalars)
            )
            setattr(self, name, value)


def merge(merger, self, lst):
    # Hack till we become selfless.
    self.__dict__ = lst[0].__dict__.copy()

    if self.Format != 3:
        return

    instancer = merger.instancer
    dev = self.DeviceTable
    if merger.deleteVariations:
        del self.DeviceTable
    if dev:
        assert dev.DeltaFormat == 0x8000
        varidx = (dev.StartSize << 16) + dev.EndSize
        delta = otRound(instancer[varidx])
        self.Coordinate += delta

    if merger.deleteVariations:
        self.Format = 1


def merge(merger, self, lst):
    # Hack till we become selfless.
    self.__dict__ = lst[0].__dict__.copy()

    if self.Format != 3:
        return

    instancer = merger.instancer
    for v in "XY":
        tableName = v + "DeviceTable"
        if not hasattr(self, tableName):
            continue
        dev = getattr(self, tableName)
        if merger.deleteVariations:
            delattr(self, tableName)
        if dev is None:
            continue

        assert dev.DeltaFormat == 0x8000
        varidx = (dev.StartSize << 16) + dev.EndSize
        delta = otRound(instancer[varidx])

        attr = v + "Coordinate"
        setattr(self, attr, getattr(self, attr) + delta)

    if merger.deleteVariations:
        self.Format = 1


def merge(merger, self, lst):
    # Hack till we become selfless.
    self.__dict__ = lst[0].__dict__.copy()

    instancer = merger.instancer
    for name, tableName in [
        ("XAdvance", "XAdvDevice"),
        ("YAdvance", "YAdvDevice"),
        ("XPlacement", "XPlaDevice"),
        ("YPlacement", "YPlaDevice"),
    ]:
        if not hasattr(self, tableName):
            continue
        dev = getattr(self, tableName)
        if merger.deleteVariations:
            delattr(self, tableName)
        if dev is None:
            continue

        assert dev.DeltaFormat == 0x8000
        varidx = (dev.StartSize << 16) + dev.EndSize
        delta = otRound(instancer[varidx])

        setattr(self, name, getattr(self, name, 0) + delta)


def merge(merger, self, lst):
    if self.Format != 1:
        raise UnsupportedFormat(merger, subtable="a baseline coordinate")
    self.Coordinate, DeviceTable = buildVarDevTable(
        merger.store_builder, [a.Coordinate for a in lst]
    )
    if DeviceTable:
        self.Format = 3
        self.DeviceTable = DeviceTable


def merge(merger, self, lst):
    if self.Format != 1:
        raise UnsupportedFormat(merger, subtable="a caret")
    self.Coordinate, DeviceTable = buildVarDevTable(
        merger.store_builder, [a.Coordinate for a in lst]
    )
    if DeviceTable:
        self.Format = 3
        self.DeviceTable = DeviceTable


def merge(merger, self, lst):
    if self.Format != 1:
        raise UnsupportedFormat(merger, subtable="an anchor")
    self.XCoordinate, XDeviceTable = buildVarDevTable(
        merger.store_builder, [a.XCoordinate for a in lst]
    )
    self.YCoordinate, YDeviceTable = buildVarDevTable(
        merger.store_builder, [a.YCoordinate for a in lst]
    )
    if XDeviceTable or YDeviceTable:
        self.Format = 3
        self.XDeviceTable = XDeviceTable
        self.YDeviceTable = YDeviceTable


def merge(merger, self, lst):
    for name, tableName in [
        ("XAdvance", "XAdvDevice"),
        ("YAdvance", "YAdvDevice"),
        ("XPlacement", "XPlaDevice"),
        ("YPlacement", "YPlaDevice"),
    ]:
        if hasattr(self, name):
            value, deviceTable = buildVarDevTable(
                merger.store_builder, [getattr(a, name, 0) for a in lst]
            )
            setattr(self, name, value)
            if deviceTable:
                setattr(self, tableName, deviceTable)


def merge(merger, self, lst):
    # ignore BaseGlyphCount, allow sparse glyph sets across masters
    out = {rec.BaseGlyph: rec for rec in self.BaseGlyphPaintRecord}
    masters = [{rec.BaseGlyph: rec for rec in m.BaseGlyphPaintRecord} for m in lst]

    for i, g in enumerate(out.keys()):
        try:
            # missing base glyphs don't participate in the merge
            merger.mergeThings(out[g], [v.get(g) for v in masters])
        except VarLibMergeError as e:
            e.stack.append(f".BaseGlyphPaintRecord[{i}]")
            e.cause["location"] = f"base glyph {g!r}"
            raise

    merger._doneBaseGlyphs = True


def merge(merger, self, lst):
    # nothing to merge for LayerList, assuming we have already merged all PaintColrLayers
    # found while traversing the paint graphs rooted at BaseGlyphPaintRecords.
    assert merger._doneBaseGlyphs, "BaseGlyphList must be merged before LayerList"
    # Simply flush the final list of layers and go home.
    self.LayerCount = len(merger.layers)
    self.Paint = merger.layers


def merge(merger, self, lst):
    fmt = merger.checkFormatEnum(self, lst, lambda fmt: not fmt.is_variable())

    if fmt is ot.PaintFormat.PaintColrLayers:
        _merge_PaintColrLayers(merger, self, lst)
        return

    varFormat = fmt.as_variable()

    varAttrs = ()
    if varFormat is not None:
        varAttrs = otBase.getVariableAttrs(type(self), varFormat)
    staticAttrs = (c.name for c in self.getConverters() if c.name not in varAttrs)

    merger.mergeAttrs(self, lst, staticAttrs)

    varIndexBase = merger.mergeVariableAttrs(self, lst, varAttrs)

    subTables = [st.value for st in self.iterSubTables()]

    # Convert table to variable if itself has variations or any subtables have
    isVariable = varIndexBase != ot.NO_VARIATION_INDEX or any(
        id(table) in merger.varTableIds for table in subTables
    )

    if isVariable:
        if varAttrs:
            # Some PaintVar* don't have any scalar attributes that can vary,
            # only indirect offsets to other variable subtables, thus have
            # no VarIndexBase of their own (e.g. PaintVarTransform)
            self.VarIndexBase = varIndexBase

        if subTables:
            # Convert Affine2x3 -> VarAffine2x3, ColorLine -> VarColorLine, etc.
            merger.convertSubTablesToVarType(self)

        assert varFormat is not None
        self.Format = int(varFormat)


def merge(merger, self, lst):
    varType = type(self).VarType

    varAttrs = otBase.getVariableAttrs(varType)
    staticAttrs = (c.name for c in self.getConverters() if c.name not in varAttrs)

    merger.mergeAttrs(self, lst, staticAttrs)

    varIndexBase = merger.mergeVariableAttrs(self, lst, varAttrs)

    if varIndexBase != ot.NO_VARIATION_INDEX:
        self.VarIndexBase = varIndexBase
        # mark as having variations so the parent table will convert to Var{Type}
        merger.varTableIds.add(id(self))


def merge(merger, self, lst):
    merger.mergeAttrs(self, lst, (c.name for c in self.getConverters()))

    if any(id(stop) in merger.varTableIds for stop in self.ColorStop):
        merger.convertSubTablesToVarType(self)
        merger.varTableIds.add(id(self))


def merge(merger, self, lst):
    # 'sparse' in that we allow non-default masters to omit ClipBox entries
    # for some/all glyphs (i.e. they don't participate)
    merger.mergeSparseDict(self, lst)


def merge(
  state: GraphState[A],
  /,
  *states: GraphState[A],
  copy: bool = False,
  recreate_variables: bool = True,
) -> A: ...


def merge(  # type: ignore[invalid-annotation]
  graphdef: GraphDef[A],
  state: tp.Any,
  /,
  *states: tp.Any,
  copy: bool = False,
  recreate_variables: bool = True,
) -> A: ...


def merge(  # type: ignore[invalid-annotation]
  graphdef_or_graphstate: GraphDef[A] | GraphState[A],
  /,
  *states: tp.Any,
  copy: bool = False,
  recreate_variables: bool = True,
) -> A:
  """The inverse of :func:`flax.nnx.split`.

  ``nnx.merge`` takes a :class:`flax.nnx.GraphDef` and one or more :class:`flax.nnx.State`'s
  and creates a new node with the same structure as the original node.

  Recall: :func:`flax.nnx.split` is used to represent a :class:`flax.nnx.Module`
  by: 1) a static ``nnx.GraphDef`` that captures its Pythonic static information;
  and 2) one or more :class:`flax.nnx.Variable` ``nnx.State``'(s) that capture
  its ``jax.Array``'s in the form of JAX pytrees.

  ``nnx.merge`` is used in conjunction with ``nnx.split`` to switch seamlessly
  between stateful and stateless representations of the graph.

  Example usage::

    >>> from flax import nnx
    >>> import jax, jax.numpy as jnp
    ...
    >>> class Foo(nnx.Module):
    ...   def __init__(self, rngs):
    ...     self.batch_norm = nnx.BatchNorm(2, rngs=rngs)
    ...     self.linear = nnx.Linear(2, 3, rngs=rngs)
    ...
    >>> node = Foo(nnx.Rngs(0))
    >>> graphdef, params, batch_stats = nnx.split(node, nnx.Param, nnx.BatchStat)
    ...
    >>> new_node = nnx.merge(graphdef, params, batch_stats)
    >>> assert isinstance(new_node, Foo)
    >>> assert isinstance(new_node.batch_norm, nnx.BatchNorm)
    >>> assert isinstance(new_node.linear, nnx.Linear)

  ``nnx.split`` and ``nnx.merge`` are primarily used to interact directly with JAX
  transformations (refer to
  `Functional API <https://flax.readthedocs.io/en/latest/nnx_basics.html#the-flax-functional-api>`__
  for more information.

  Args:
    graphdef_or_graphstate: A :class:`flax.nnx.GraphDef` or :class:`flax.nnx.GraphState` object.
    *states: Additional :class:`flax.nnx.State` or :class:`flax.nnx.GraphState` objects.
    copy: Whether to create new copies of the Variables in the states, defaults to ``False``.
  Returns:
    The merged :class:`flax.nnx.Module`.
  """
  if isinstance(graphdef_or_graphstate, GraphState):
    graphdef = graphdef_or_graphstate._graphdef
    all_states = (graphdef_or_graphstate, *states)
    for graph_state in all_states:
      if not isinstance(graph_state, GraphState):
        raise ValueError(f'Expected GraphState object, got {type(graph_state)}')
      if graph_state._graphdef != graphdef:
        raise ValueError('GraphDef must be the same for all GraphState objects')
  elif isinstance(graphdef_or_graphstate, GraphDef):
    graphdef = graphdef_or_graphstate
    all_states = states
  else:
    raise TypeError(f'Expected a GraphDef or GraphState object, got: {graphdef_or_graphstate!r}')
  if len(all_states) == 0:
    raise TypeError("merge() missing 1 required positional argument: 'state'")
  if isinstance(state := all_states[0], list):
    if len(all_states) != 1:
      raise ValueError(f'Only one state can be passed as a list.')
    _state = state
  else:
    _state = _merge_to_flat_state(all_states)
  node = unflatten(graphdef, _state, copy_variables=copy, recreate_variables=recreate_variables)
  return node

