
def get_grouper(
    obj: NDFrameT,
    key=None,
    level=None,
    sort: bool = True,
    observed: bool = False,
    validate: bool = True,
    dropna: bool = True,
) -> tuple[ops.BaseGrouper, frozenset[Hashable], NDFrameT]:
    """
    Create and return a BaseGrouper, which is an internal
    mapping of how to create the grouper indexers.
    This may be composed of multiple Grouping objects, indicating
    multiple groupers

    Groupers are ultimately index mappings. They can originate as:
    index mappings, keys to columns, functions, or Groupers

    Groupers enable local references to level,sort, while
    the passed in level, and sort are 'global'.

    This routine tries to figure out what the passing in references
    are and then creates a Grouping for each one, combined into
    a BaseGrouper.

    If observed & we have a categorical grouper, only show the observed
    values.

    If validate, then check for key/level overlaps.

    """
    group_axis = obj.index

    # validate that the passed single level is compatible with the passed
    # index of the object
    if level is not None:
        # TODO: These if-block and else-block are almost same.
        # MultiIndex instance check is removable, but it seems that there are
        # some processes only for non-MultiIndex in else-block,
        # eg. `obj.index.name != level`. We have to consider carefully whether
        # these are applicable for MultiIndex. Even if these are applicable,
        # we need to check if it makes no side effect to subsequent processes
        # on the outside of this condition.
        # (GH 17621)
        if isinstance(group_axis, MultiIndex):
            if is_list_like(level) and len(level) == 1:
                level = level[0]

            if key is None and is_scalar(level):
                # Get the level values from group_axis
                key = group_axis.get_level_values(level)
                level = None

        else:
            # allow level to be a length-one list-like object
            # (e.g., level=[0])
            # GH 13901
            if is_list_like(level):
                nlevels = len(level)
                if nlevels == 1:
                    level = level[0]
                elif nlevels == 0:
                    raise ValueError("No group keys passed!")
                else:
                    raise ValueError("multiple levels only valid with MultiIndex")

            if isinstance(level, str):
                if obj.index.name != level:
                    raise ValueError(f"level name {level} is not the name of the index")
            elif level > 0 or level < -1:
                raise ValueError("level > 0 or level < -1 only valid with MultiIndex")

            # NOTE: `group_axis` and `group_axis.get_level_values(level)`
            # are same in this section.
            level = None
            key = group_axis

    # a passed-in Grouper, directly convert
    if isinstance(key, Grouper):
        grouper, obj = key._get_grouper(obj, validate=False, observed=observed)
        if key.key is None:
            return grouper, frozenset(), obj
        else:
            return grouper, frozenset({key.key}), obj

    # already have a BaseGrouper, just return it
    elif isinstance(key, ops.BaseGrouper):
        return key, frozenset(), obj

    if not isinstance(key, list):
        keys = [key]
        match_axis_length = False
    else:
        keys = key
        match_axis_length = len(keys) == len(group_axis)

    # what are we after, exactly?
    any_callable = any(callable(g) or isinstance(g, dict) for g in keys)
    any_groupers = any(isinstance(g, (Grouper, Grouping)) for g in keys)
    any_arraylike = any(
        isinstance(g, (list, tuple, Series, Index, np.ndarray)) for g in keys
    )

    # is this an index replacement?
    if (
        not any_callable
        and not any_arraylike
        and not any_groupers
        and match_axis_length
        and level is None
    ):
        if isinstance(obj, DataFrame):
            all_in_columns_index = all(
                g in obj.columns or g in obj.index.names for g in keys
            )
        else:
            assert isinstance(obj, Series)
            all_in_columns_index = all(g in obj.index.names for g in keys)

        if not all_in_columns_index:
            keys = [com.asarray_tuplesafe(keys)]

    if isinstance(level, (tuple, list)):
        if key is None:
            keys = [None] * len(level)
        levels = level
    else:
        levels = [level] * len(keys)

    groupings: list[Grouping] = []
    exclusions: set[Hashable] = set()

    # if the actual grouper should be obj[key]
    def is_in_axis(key) -> bool:
        if not _is_label_like(key):
            if obj.ndim == 1:
                return False

            # items -> .columns for DataFrame, .index for Series
            items = obj.axes[-1]
            try:
                items.get_loc(key)
            except (KeyError, TypeError, InvalidIndexError):
                # TypeError shows up here if we pass e.g. an Index
                return False

        return True

    # if the grouper is obj[name]
    def is_in_obj(gpr) -> bool:
        if not hasattr(gpr, "name"):
            return False
        # We check the references to determine if the
        # series is part of the object
        try:
            obj_gpr_column = obj[gpr.name]
        except (KeyError, IndexError, InvalidIndexError, OutOfBoundsDatetime):
            return False
        if isinstance(gpr, Series) and isinstance(obj_gpr_column, Series):
            return gpr._mgr.references_same_values(obj_gpr_column._mgr, 0)
        return False

    for gpr, level in zip(keys, levels, strict=True):
        if is_in_obj(gpr):  # df.groupby(df['name'])
            in_axis = True
            exclusions.add(gpr.name)

        elif is_in_axis(gpr):  # df.groupby('name')
            if obj.ndim != 1 and gpr in obj:
                if validate:
                    obj._check_label_or_level_ambiguity(gpr, axis=0)
                in_axis, name, gpr = True, gpr, obj[gpr]
                if gpr.ndim != 1:
                    # non-unique columns; raise here to get the name in the
                    # exception message
                    raise ValueError(f"Grouper for '{name}' not 1-dimensional")
                exclusions.add(name)
            elif obj._is_level_reference(gpr, axis=0):
                in_axis, level, gpr = False, gpr, None
            else:
                raise KeyError(gpr)
        elif isinstance(gpr, Grouper) and gpr.key is not None:
            # Add key to exclusions
            exclusions.add(gpr.key)
            in_axis = True
        else:
            in_axis = False

        # create the Grouping
        # allow us to passing the actual Grouping as the gpr
        ping = (
            Grouping(
                group_axis,
                gpr,
                obj=obj,
                level=level,
                sort=sort,
                observed=observed,
                in_axis=in_axis,
                dropna=dropna,
            )
            if not isinstance(gpr, Grouping)
            else gpr
        )

        groupings.append(ping)

    if len(groupings) == 0 and len(obj):
        raise ValueError("No group keys passed!")
    if len(groupings) == 0:
        groupings.append(Grouping(default_index(0), np.array([], dtype=np.intp)))

    # create the internals grouper
    grouper = ops.BaseGrouper(group_axis, groupings, sort=sort, dropna=dropna)
    return grouper, frozenset(exclusions), obj

