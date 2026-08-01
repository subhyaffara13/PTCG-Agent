
def clean_reindex_fill_method(method) -> ReindexMethod | None:
    if method is None:
        return None
    return clean_fill_method(method, allow_nearest=True)

