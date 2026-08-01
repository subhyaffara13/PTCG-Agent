
def _maybe_convert_string_index_to_object(index: pd.Index) -> pd.Index | None:
    if isinstance(index, pd.MultiIndex):
        if any(
            isinstance(level.dtype, pd.StringDtype) and level.dtype.na_value is np.nan
            for level in index.levels
        ):
            new_levels = []
            for level in index.levels:
                new_level = _maybe_convert_string_to_object(level)
                if new_level is not None:
                    new_levels.append(new_level)
                else:
                    new_levels.append(level)
            return index.set_levels(new_levels)
        return None

    else:
        return cast("pd.Index | None", _maybe_convert_string_to_object(index))

