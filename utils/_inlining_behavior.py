
def _inlining_behavior(
    def_ref: core_schema.DefinitionReferenceSchema,
) -> Literal['inline', 'keep', 'preserve_metadata']:
    """Determine the inlining behavior of the `'definition-ref'` schema.

    - If no `'serialization'` schema and no metadata is attached, the schema can safely be inlined.
    - If it has metadata but only related to the deferred discriminator application, it can be inlined
      provided that such metadata is kept.
    - Otherwise, the schema should not be inlined. Doing so would remove the `'serialization'` schema or metadata.
    """
    if 'serialization' in def_ref:
        return 'keep'
    metadata = def_ref.get('metadata')
    if not metadata:
        return 'inline'
    if len(metadata) == 1 and 'pydantic_internal_union_discriminator' in metadata:
        return 'preserve_metadata'
    return 'keep'

