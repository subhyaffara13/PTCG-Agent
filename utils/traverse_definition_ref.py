
def traverse_definition_ref(def_ref_schema: DefinitionReferenceSchema, ctx: GatherContext) -> None:
    schema_ref = def_ref_schema['schema_ref']

    if schema_ref not in ctx.collected_references:
        definition = ctx.definitions.get(schema_ref)
        if definition is None:
            raise MissingDefinitionError(schema_ref)

        # The `'definition-ref'` schema was only encountered once, make it
        # a candidate to be inlined:
        ctx.collected_references[schema_ref] = def_ref_schema
        traverse_schema(definition, ctx)
        if 'serialization' in def_ref_schema:
            traverse_schema(def_ref_schema['serialization'], ctx)
        traverse_metadata(def_ref_schema, ctx)
    else:
        # The `'definition-ref'` schema was already encountered, meaning
        # the previously encountered schema (and this one) can't be inlined:
        ctx.collected_references[schema_ref] = None

