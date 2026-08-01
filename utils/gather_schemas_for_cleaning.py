
def gather_schemas_for_cleaning(schema: CoreSchema, definitions: dict[str, CoreSchema]) -> GatherResult:
    """Traverse the core schema and definitions and return the necessary information for schema cleaning.

    During the core schema traversing, any `'definition-ref'` schema is:

    - Validated: the reference must point to an existing definition. If this is not the case, a
      `MissingDefinitionError` exception is raised.
    - Stored in the context: the actual reference is stored in the context. Depending on whether
      the `'definition-ref'` schema is encountered more that once, the schema itself is also
      saved in the context to be inlined (i.e. replaced by the definition it points to).
    """
    context = GatherContext(definitions)
    traverse_schema(schema, context)

    return {
        'collected_references': context.collected_references,
        'deferred_discriminator_schemas': context.deferred_discriminator_schemas,
    }

