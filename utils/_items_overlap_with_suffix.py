
def _items_overlap_with_suffix(
    left: Index, right: Index, suffixes: Suffixes
) -> tuple[Index, Index]:
    """
    Suffixes type validation.

    If two indices overlap, add suffixes to overlapping entries.

    If corresponding suffix is empty, the entry is simply converted to string.

    """
    if not is_list_like(suffixes, allow_sets=False) or isinstance(suffixes, dict):
        raise TypeError(
            f"Passing 'suffixes' as a {type(suffixes)}, is not supported. "
            "Provide 'suffixes' as a tuple instead."
        )

    to_rename = left.intersection(right)
    if len(to_rename) == 0:
        return left, right

    lsuffix, rsuffix = suffixes

    if not lsuffix and not rsuffix:
        raise ValueError(f"columns overlap but no suffix specified: {to_rename}")

    def renamer(x, suffix: str | None):
        """
        Rename the left and right indices.

        If there is overlap, and suffix is not None, add
        suffix, otherwise, leave it as-is.

        Parameters
        ----------
        x : original column name
        suffix : str or None

        Returns
        -------
        x : renamed column name
        """
        if x in to_rename and suffix is not None:
            return f"{x}{suffix}"
        return x

    lrenamer = partial(renamer, suffix=lsuffix)
    rrenamer = partial(renamer, suffix=rsuffix)

    llabels = left._transform_index(lrenamer)
    rlabels = right._transform_index(rrenamer)

    dups = []
    if not llabels.is_unique:
        # Only warn when duplicates are caused because of suffixes, already duplicated
        # columns in origin should not warn
        dups.extend(llabels[(llabels.duplicated()) & (~left.duplicated())].tolist())
    if not rlabels.is_unique:
        dups.extend(rlabels[(rlabels.duplicated()) & (~right.duplicated())].tolist())
    # Suffix addition creates duplicate to pre-existing column name
    dups.extend(llabels.intersection(right.difference(to_rename)).tolist())
    dups.extend(rlabels.intersection(left.difference(to_rename)).tolist())
    if dups:
        raise MergeError(
            f"Passing 'suffixes' which cause duplicate columns {set(dups)} is "
            "not allowed.",
        )

    return llabels, rlabels

