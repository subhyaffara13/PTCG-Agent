
def _get_inner_meta(
    maybe_subclass_meta: SubclassMeta | None,
    fw_metadata: ViewAndMutationMeta,
) -> ViewAndMutationMeta:
    """
    Util to get view and mutation metadata.
    """
    return (
        fw_metadata if maybe_subclass_meta is None else maybe_subclass_meta.fw_metadata
    )

