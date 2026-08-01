
def _factory(definition, handlers, formats={}, use_default=True, use_formats=True, detailed_exceptions=True):
    resolver = RefResolver.from_schema(definition, handlers=handlers, store={})
    code_generator = _get_code_generator_class(definition)(
        definition,
        resolver=resolver,
        formats=formats,
        use_default=use_default,
        use_formats=use_formats,
        detailed_exceptions=detailed_exceptions,
    )
    return resolver, code_generator

