
def _build_tags_expr(available_keys: list[str]) -> pl.Expr:
    """Build a Polars expression that produces a JSON Tags string per row.

    Uses ``pl.struct`` + ``map_elements`` to avoid materialising the entire
    DataFrame to a list of Python dicts.  The JSON serialisation callback
    still runs in Python (GIL-bound), but struct-packing and loop dispatch
    are handled by Polars' Rust engine.
    """

    def _struct_to_json(row: dict) -> str:
        tags = {k: str(v) for k, v in row.items() if v is not None}
        return json.dumps(tags) if tags else "{}"

    return (
        pl.struct(available_keys)
        .map_elements(_struct_to_json, return_dtype=pl.String)
        .alias("Tags")
    )

