
def transform_imports_without_grouping(
    builder: IRBuilder, group: list[tuple[str, str | None, int]]
) -> None:
    globals = builder.load_globals_dict()
    for mod_id, as_name, line in group:
        builder.gen_import(mod_id, line)
        globals_id, globals_name = import_globals_id_and_name(mod_id, as_name)
        builder.gen_method_call(
            globals,
            "__setitem__",
            [builder.load_str(globals_name), builder.get_module(globals_id, line)],
            result_type=None,
            line=line,
        )

