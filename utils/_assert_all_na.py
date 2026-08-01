
def _assert_all_na(join_chunk, source_columns, join_col):
    for c in source_columns:
        if c in join_col:
            continue
        assert join_chunk[c].isna().all()

