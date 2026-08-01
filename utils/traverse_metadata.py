
def traverse_metadata(schema: AllSchemas, ctx: GatherContext) -> None:
    meta = schema.get('metadata')
    if meta is not None and 'pydantic_internal_union_discriminator' in meta:
        ctx.deferred_discriminator_schemas.append(schema)  # pyright: ignore[reportArgumentType]

