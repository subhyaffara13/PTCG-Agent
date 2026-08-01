
def update_core_metadata(
    core_metadata: Any,
    /,
    *,
    pydantic_js_functions: list[GetJsonSchemaFunction] | None = None,
    pydantic_js_annotation_functions: list[GetJsonSchemaFunction] | None = None,
    pydantic_js_updates: JsonDict | None = None,
    pydantic_js_extra: JsonDict | JsonSchemaExtraCallable | None = None,
) -> None:
    from ..json_schema import PydanticJsonSchemaWarning

    """Update CoreMetadata instance in place. When we make modifications in this function, they
    take effect on the `core_metadata` reference passed in as the first (and only) positional argument.

    First, cast to `CoreMetadata`, then finish with a cast to `dict[str, Any]` for core schema compatibility.
    We do this here, instead of before / after each call to this function so that this typing hack
    can be easily removed if/when we move `CoreMetadata` to `pydantic-core`.

    For parameter descriptions, see `CoreMetadata` above.
    """
    core_metadata = cast(CoreMetadata, core_metadata)

    if pydantic_js_functions:
        core_metadata.setdefault('pydantic_js_functions', []).extend(pydantic_js_functions)

    if pydantic_js_annotation_functions:
        core_metadata.setdefault('pydantic_js_annotation_functions', []).extend(pydantic_js_annotation_functions)

    if pydantic_js_updates:
        if (existing_updates := core_metadata.get('pydantic_js_updates')) is not None:
            core_metadata['pydantic_js_updates'] = {**existing_updates, **pydantic_js_updates}
        else:
            core_metadata['pydantic_js_updates'] = pydantic_js_updates

    if pydantic_js_extra is not None:
        existing_pydantic_js_extra = core_metadata.get('pydantic_js_extra')
        if existing_pydantic_js_extra is None:
            core_metadata['pydantic_js_extra'] = pydantic_js_extra
        if isinstance(existing_pydantic_js_extra, dict):
            if isinstance(pydantic_js_extra, dict):
                core_metadata['pydantic_js_extra'] = {**existing_pydantic_js_extra, **pydantic_js_extra}
            if callable(pydantic_js_extra):
                warn(
                    'Composing `dict` and `callable` type `json_schema_extra` is not supported.'
                    'The `callable` type is being ignored.'
                    "If you'd like support for this behavior, please open an issue on pydantic.",
                    PydanticJsonSchemaWarning,
                )
        if callable(existing_pydantic_js_extra):
            # if ever there's a case of a callable, we'll just keep the last json schema extra spec
            core_metadata['pydantic_js_extra'] = pydantic_js_extra

