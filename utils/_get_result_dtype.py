
def _get_result_dtype(
    to_concat: Sequence[ArrayLike], non_empties: Sequence[ArrayLike]
) -> tuple[bool, set[str], DtypeObj | None]:
    target_dtype = None

    dtypes = {obj.dtype for obj in to_concat}
    kinds = {obj.dtype.kind for obj in to_concat}

    any_ea = any(not isinstance(x, np.ndarray) for x in to_concat)
    if any_ea:
        # i.e. any ExtensionArrays

        # we ignore axis here, as internally concatting with EAs is always
        # for axis=0
        if len(dtypes) != 1:
            target_dtype = find_common_type([x.dtype for x in to_concat])
            target_dtype = common_dtype_categorical_compat(to_concat, target_dtype)

    elif not len(non_empties):
        # we have all empties, but may need to coerce the result dtype to
        # object if we have non-numeric type operands (numpy would otherwise
        # cast this to float)
        if len(kinds) != 1:
            if not len(kinds - {"i", "u", "f"}) or not len(kinds - {"b", "i", "u"}):
                # let numpy coerce
                pass
            else:
                # coerce to object
                target_dtype = np.dtype(object)
                kinds = {"o"}
    elif "b" in kinds and len(kinds) > 1:
        # GH#21108, GH#45101
        target_dtype = np.dtype(object)
        kinds = {"o"}
    else:
        # error: Argument 1 to "np_find_common_type" has incompatible type
        # "*Set[Union[ExtensionDtype, Any]]"; expected "dtype[Any]"
        target_dtype = np_find_common_type(*dtypes)  # type: ignore[arg-type]

    return any_ea, kinds, target_dtype

