
def transform_import_from_buckets(
    builder: IRBuilder,
    module_id: str,
    names: list[str],
    as_names: list[str],
    line: int,
    parent_is_native: bool,
) -> None:
    """Handle 'from module_id import names' by dispatching each bucket to the right strategy."""
    buckets = classify_import_from(builder, module_id, names, as_names, parent_is_native)
    module = None
    for bucket in buckets:
        if bucket.kind == IMPORT_NATIVE_SUBMODULE:
            group: list[tuple[str, str | None, int]] = [
                (f"{module_id}.{name}", as_name, line)
                for name, as_name in zip(bucket.names, bucket.as_names)
            ]
            transform_imports_without_grouping(builder, group)
        elif bucket.kind == IMPORT_NATIVE_ATTR:
            builder.gen_import(module_id, line)
            names_literal = builder.add(LoadLiteral(tuple(bucket.names), object_rprimitive))
            if bucket.as_names == bucket.names:
                as_names_literal = names_literal
            else:
                as_names_literal = builder.add(
                    LoadLiteral(tuple(bucket.as_names), object_rprimitive)
                )
            builder.call_c(
                get_native_attrs_op,
                [
                    builder.load_str(module_id),
                    names_literal,
                    as_names_literal,
                    builder.load_globals_dict(),
                ],
                line,
            )
        else:
            assert bucket.kind == IMPORT_NON_NATIVE
            # Note that we miscompile import from inside of functions here,
            # since that case *shouldn't* load everything into the globals dict.
            # This probably doesn't matter much and the code runs basically right.
            names_literal = builder.add(LoadLiteral(tuple(bucket.names), object_rprimitive))
            if bucket.as_names == bucket.names:
                as_names_literal = names_literal
            else:
                as_names_literal = builder.add(
                    LoadLiteral(tuple(bucket.as_names), object_rprimitive)
                )
            module = builder.call_c(
                import_from_many_op,
                [
                    builder.load_str(module_id),
                    names_literal,
                    as_names_literal,
                    builder.load_globals_dict(),
                ],
                line,
            )
    if module is not None:
        builder.add(InitStatic(module, module_id, namespace=NAMESPACE_MODULE))

