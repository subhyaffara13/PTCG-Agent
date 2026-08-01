
def non_empty_field_validator(df: pd.DataFrame, field: str = "completion") -> Remediation:
    """
    This validator will ensure that no completion is empty.
    """
    necessary_msg = None
    necessary_fn = None  # type: ignore
    immediate_msg = None

    if df[field].apply(lambda x: x == "").any() or df[field].isnull().any():
        empty_rows = (df[field] == "") | (df[field].isnull())
        empty_indexes = df.reset_index().index[empty_rows].tolist()
        immediate_msg = f"\n- `{field}` column/key should not contain empty strings. These are rows: {empty_indexes}"

        def necessary_fn(x: Any) -> Any:
            return x[x[field] != ""].dropna(subset=[field])

        necessary_msg = f"Remove {len(empty_indexes)} rows with empty {field}s"

    return Remediation(
        name=f"empty_{field}",
        immediate_msg=immediate_msg,
        necessary_msg=necessary_msg,
        necessary_fn=necessary_fn,
    )

