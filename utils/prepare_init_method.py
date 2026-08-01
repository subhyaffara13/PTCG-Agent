
def prepare_init_method(cdef: ClassDef, ir: ClassIR, module_name: str, mapper: Mapper) -> None:
    # Set up a constructor decl
    init_node = cdef.info["__init__"].node

    new_node: SymbolNode | None = None
    new_symbol = cdef.info.get("__new__")
    # We are only interested in __new__ method defined in a user-defined class,
    # so we ignore it if it comes from a builtin type. It's usually builtins.object
    # but could also be builtins.type for metaclasses so we detect the prefix which
    # matches both.
    if new_symbol and new_symbol.fullname and not new_symbol.fullname.startswith("builtins."):
        new_node = new_symbol.node
    if isinstance(new_node, (Decorator, OverloadedFuncDef)):
        new_node = get_func_def(new_node)
    if not ir.is_trait and not ir.builtin_base and isinstance(init_node, FuncDef):
        init_sig = mapper.fdef_to_sig(init_node, True)
        args_match = True
        if isinstance(new_node, FuncDef):
            new_sig = mapper.fdef_to_sig(new_node, True)
            args_match = check_matching_args(init_sig, new_sig)

        defining_ir = mapper.type_to_ir.get(init_node.info)
        # If there is a nontrivial __init__ that wasn't defined in an
        # extension class, we need to make the constructor take *args,
        # **kwargs so it can call tp_init.
        if (
            (
                defining_ir is None
                or not defining_ir.is_ext_class
                or cdef.info["__init__"].plugin_generated
            )
            and init_node.info.fullname != "builtins.object"
        ) or not args_match:
            init_sig = FuncSignature(
                [
                    init_sig.args[0],
                    RuntimeArg("args", tuple_rprimitive, ARG_STAR),
                    RuntimeArg("kwargs", dict_rprimitive, ARG_STAR2),
                ],
                init_sig.ret_type,
            )

        last_arg = len(init_sig.args) - init_sig.num_bitmap_args
        ctor_sig = FuncSignature(init_sig.args[1:last_arg], RInstance(ir))
        ir.ctor = FuncDecl(cdef.name, None, module_name, ctor_sig)
        mapper.func_to_decl[cdef.info] = ir.ctor

