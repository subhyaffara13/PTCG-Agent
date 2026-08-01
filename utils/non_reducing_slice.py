
def non_reducing_slice(slice_: Subset):
    """
    Ensure that a slice doesn't reduce to a Series or Scalar.

    Any user-passed `subset` should have this called on it
    to make sure we're always working with DataFrames.
    """
    # default to column slice, like DataFrame
    # ['A', 'B'] -> IndexSlices[:, ['A', 'B']]
    kinds = (ABCSeries, np.ndarray, Index, list, str)
    if isinstance(slice_, kinds):
        slice_ = IndexSlice[:, slice_]

    def pred(part) -> bool:
        """
        Returns
        -------
        bool
            True if slice does *not* reduce,
            False if `part` is a tuple.
        """
        # true when slice does *not* reduce, False when part is a tuple,
        # i.e. MultiIndex slice
        if isinstance(part, tuple):
            # GH#39421 check for sub-slice:
            return any((isinstance(s, slice) or is_list_like(s)) for s in part)
        else:
            return isinstance(part, slice) or is_list_like(part)

    if not is_list_like(slice_):
        if not isinstance(slice_, slice):
            # a 1-d slice, like df.loc[1]
            slice_ = [[slice_]]
        else:
            # slice(a, b, c)
            slice_ = [slice_]  # to tuplize later
    else:
        # error: Item "slice" of "Union[slice, Sequence[Any]]" has no attribute
        # "__iter__" (not iterable) -> is specifically list_like in conditional
        slice_ = [p if pred(p) else [p] for p in slice_]  # type: ignore[union-attr]
    return tuple(slice_)

