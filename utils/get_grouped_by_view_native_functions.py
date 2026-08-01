
def get_grouped_by_view_native_functions(
    native_functions: Sequence[NativeFunction],
) -> Sequence[NativeFunction | NativeFunctionsViewGroup]:
    def maybe_create_view_group(
        d: dict[ViewSchemaKind | SchemaKind, NativeFunction],
    ) -> list[NativeFunction | NativeFunctionsViewGroup]:
        funcs: list[NativeFunction | NativeFunctionsViewGroup] = []
        if ViewSchemaKind.aliasing in d:
            view = d.pop(ViewSchemaKind.aliasing)
            view_inplace = d.pop(ViewSchemaKind.aliasing_inplace, None)
            view_copy = d.pop(SchemaKind.functional, None)

            funcs.append(
                NativeFunctionsViewGroup(
                    view=view,
                    view_copy=view_copy,
                    view_inplace=view_inplace,
                )
            )
        # Take the remaining functions that weren't part of the view group
        # and emit them separately
        funcs.extend(d.values())
        return funcs

    grouped_by_views: dict[
        FunctionSchema, dict[SchemaKind | ViewSchemaKind, NativeFunction]
    ] = defaultdict(dict)
    for f in native_functions:
        schema = f.func.view_signature()
        view_kind: ViewSchemaKind = f.view_schema_kind
        # We need to group up ops relevant to the same "view", consisting of:
        # view op (ViewSchemaKind.aliasing)
        # view_inplace op (ViewSchemaKind.aliasing_inplace)
        # view_copy op (SchemaKind.functional)
        if view_kind == ViewSchemaKind.non_aliasing:
            kind = f.func.kind()
            if kind in grouped_by_views[schema]:
                raise AssertionError(
                    f"Duplicate schema kind {kind} in {grouped_by_views[schema].keys()}"
                )
            grouped_by_views[schema][kind] = f
        else:
            if view_kind in grouped_by_views[schema]:
                raise AssertionError(
                    f"{view_kind} already in {grouped_by_views[schema].keys()}"
                )
            grouped_by_views[schema][view_kind] = f

    return list(concatMap(maybe_create_view_group, grouped_by_views.values()))

