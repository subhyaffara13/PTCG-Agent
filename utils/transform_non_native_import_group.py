
def transform_non_native_import_group(
    builder: IRBuilder, group: list[tuple[str, str | None, int]]
) -> None:
    """Transform a group of import statements that target non-native modules."""
    modules = []
    static_ptrs = []
    # To show the right line number on failure, we have to add the traceback
    # entry within the helper function (which is admittedly ugly). To drive
    # this, we need the line number corresponding to each module.
    mod_lines = []
    first_line = group[0][2] if group else NO_TRACEBACK_LINE_NO
    for mod_id, as_name, line in group:
        builder.imports[mod_id] = None
        modules.append((mod_id, *import_globals_id_and_name(mod_id, as_name)))
        mod_static = LoadStatic(object_rprimitive, mod_id, namespace=NAMESPACE_MODULE)
        static_ptrs.append(builder.add(LoadAddress(object_pointer_rprimitive, mod_static)))
        mod_lines.append(Integer(line, c_pyssize_t_rprimitive))

    static_array_ptr = builder.builder.setup_rarray(
        object_pointer_rprimitive, static_ptrs, first_line
    )
    import_line_ptr = builder.builder.setup_rarray(c_pyssize_t_rprimitive, mod_lines, first_line)
    builder.call_c(
        import_many_op,
        [
            builder.add(LoadLiteral(tuple(modules), object_rprimitive)),
            static_array_ptr,
            builder.load_globals_dict(),
            builder.load_str(builder.module_path),
            builder.load_str(builder.fn_info.name),
            import_line_ptr,
        ],
        NO_TRACEBACK_LINE_NO,
    )

