
def _dispatch_dynamic_index_list(
    indices: _Union[DynamicIndexList, ArrayAttr],
) -> _Tuple[_List[ValueLike], _Union[_List[int], ArrayAttr], _List[bool]]:
    """Dispatches a list of indices to the appropriate form.

    This is similar to the custom `DynamicIndexList` directive upstream:
    provided indices may be in the form of dynamic SSA values or static values,
    and they may be scalable (i.e., as a singleton list) or not. This function
    dispatches each index into its respective form. It also extracts the SSA
    values and static indices from various similar structures, respectively.
    """
    dynamic_indices = []
    static_indices = [ShapedType.get_dynamic_size()] * len(indices)
    scalable_indices = [False] * len(indices)

    # ArrayAttr: Extract index values.
    if isinstance(indices, ArrayAttr):
        indices = [idx for idx in indices]

    def process_nonscalable_index(i, index):
        """Processes any form of non-scalable index.

        Returns False if the given index was scalable and thus remains
        unprocessed; True otherwise.
        """
        if isinstance(index, int):
            static_indices[i] = index
        elif isinstance(index, IntegerAttr):
            static_indices[i] = index.value  # pytype: disable=attribute-error
        elif isinstance(index, (Operation, Value, OpView)):
            dynamic_indices.append(index)
        else:
            return False
        return True

    # Process each index at a time.
    for i, index in enumerate(indices):
        if not process_nonscalable_index(i, index):
            # If it wasn't processed, it must be a scalable index, which is
            # provided as a _Sequence of one value, so extract and process that.
            scalable_indices[i] = True
            assert len(index) == 1
            ret = process_nonscalable_index(i, index[0])
            assert ret

    return dynamic_indices, static_indices, scalable_indices

