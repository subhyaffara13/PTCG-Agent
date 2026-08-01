
def compile_modules_to_ir(
    result: BuildResult, mapper: Mapper, compiler_options: CompilerOptions, errors: Errors
) -> ModuleIRs:
    """Compile a collection of modules into ModuleIRs.

    The modules to compile are specified as part of mapper's group_map.

    Returns the IR of the modules.
    """
    deser_ctx = DeserMaps({}, {})
    modules = {}

    # Process the graph by SCC in topological order, like we do in mypy.build
    for scc in sorted_components(result.graph):
        scc_states = [result.graph[id] for id in sorted(scc.mod_ids)]
        trees = [st.tree for st in scc_states if st.id in mapper.group_map and st.tree]

        if not trees:
            continue

        fresh = all(id not in result.manager.rechecked_modules for id in scc.mod_ids)
        if fresh:
            load_scc_from_cache(trees, result, mapper, deser_ctx)
        else:
            scc_ir = compile_scc_to_ir(trees, result, mapper, compiler_options, errors)
            modules.update(scc_ir)
            # A later SCC loaded from cache may reference classes/functions
            # defined in this freshly-built SCC; populate deser_ctx so the
            # cached IR deserializer can resolve those cross-SCC references.
            for module_ir in scc_ir.values():
                for cl in module_ir.classes:
                    deser_ctx.classes.setdefault(cl.fullname, cl)
                for fn in module_ir.functions:
                    deser_ctx.functions.setdefault(fn.decl.id, fn)

    return modules

