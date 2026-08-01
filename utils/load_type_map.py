
def load_type_map(mapper: Mapper, modules: list[MypyFile], deser_ctx: DeserMaps) -> None:
    """Populate a Mapper with deserialized IR from a list of modules."""
    for module in modules:
        for node in module.names.values():
            if (
                isinstance(node.node, TypeInfo)
                and is_from_module(node.node, module)
                and not node.node.is_newtype
                and not node.node.is_named_tuple
                and node.node.typeddict_type is None
            ):
                # Some TypeInfo entries are mypy-synthetic (e.g. anonymous
                # intersection classes like "<subclass of X and Y>") and have
                # no corresponding mypyc ClassIR. Skip those rather than
                # aborting the whole cache load.
                ir = deser_ctx.classes.get(node.node.fullname)
                if ir is None:
                    continue
                mapper.type_to_ir[node.node] = ir
                mapper.symbol_fullnames.add(node.node.fullname)
                # Trait/builtin-base classes have an ir.ctor FuncDecl
                # but no emitted CPyDef_<ctor>, so a cross-group direct
                # call would hit an undefined symbol. Mirror the skip
                # in prepare_init_method.
                if not ir.is_trait and not ir.builtin_base:
                    mapper.func_to_decl[node.node] = ir.ctor

    for module in modules:
        for func in get_module_func_defs(module):
            func_id = get_id_from_name(func.name, func.fullname, func.line)
            mapper.func_to_decl[func] = deser_ctx.functions[func_id].decl

