
def make_runtime_safe(
    fw_metadata: ViewAndMutationMeta,
    maybe_subclass_meta: SubclassMeta | None,
) -> None:
    """
    Calls make_runtime_safe on all ViewAndMutationMetas.
    Modifies both arguments. Allows ViewAndMutationMetas to
    be safely cached in AOTAutogradCache.
    """
    fw_metadata.make_runtime_safe()
    if maybe_subclass_meta is not None:
        maybe_subclass_meta.fw_metadata.make_runtime_safe()
        if maybe_subclass_meta.grad_input_metas:
            for meta in maybe_subclass_meta.grad_input_metas:
                if isinstance(meta, SubclassCreationMeta):
                    meta.make_runtime_safe()

