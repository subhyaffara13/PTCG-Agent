
def _get_codes_for_values(
    values: Index | Series | ExtensionArray | np.ndarray,
    categories: Index,
) -> np.ndarray:
    """
    utility routine to turn values into codes given the specified categories

    If `values` is known to be a Categorical, use recode_for_categories instead.
    """
    codes = categories.get_indexer_for(values)
    wrong = (codes == -1) & ~isna(values)
    if wrong.any():
        warnings.warn(
            "Constructing a Categorical with a dtype and values containing "
            "non-null entries not in that dtype's categories is deprecated "
            "and will raise in a future version.",
            Pandas4Warning,
            stacklevel=find_stack_level(),
        )
    return coerce_indexer_dtype(codes, categories)

