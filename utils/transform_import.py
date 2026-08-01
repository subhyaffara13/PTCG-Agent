
def transform_import(builder: IRBuilder, node: Import) -> None:
    if node.is_mypy_only:
        return

    # Imports (not from imports!) are processed in an odd way so they can be
    # table-driven and compact. Here's how it works:
    #
    # Import nodes are divided in groups (in the prebuild visitor). Each group
    # consists of consecutive Import nodes:
    #
    #   import mod         <| group #1
    #   import mod2         |
    #
    #   def foo() -> None:
    #       import mod3    <- group #2 (*)
    #
    #   import mod4        <| group #3
    #   import mod5         |
    #
    # Every time we encounter the first import of a group, build IR to import
    # all modules in the group. Native same-group imports are handled individually,
    # while non-native imports use a table-driven helper for compactness.

    if not node.is_top_level:
        # (*) Unless the import is within a function. In that case, prioritize
        # speed over codesize when generating IR.
        group = [(mod_id, as_id, node.line) for mod_id, as_id in node.ids]
        transform_imports_without_grouping(builder, group)
        return

    if node not in builder.module_import_groups:
        return

    group_nodes = builder.module_import_groups[node]
    subgroups = split_import_group_to_python_and_native(builder, group_nodes)
    for subgroup, is_native in subgroups:
        if is_native:
            transform_imports_without_grouping(builder, subgroup)
        else:
            transform_non_native_import_group(builder, subgroup)

