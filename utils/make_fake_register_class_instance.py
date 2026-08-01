
def make_fake_register_class_instance(
    api: CheckerPluginInterface, type_args: Sequence[Type]
) -> Instance:
    defn = ClassDef(SINGLEDISPATCH_REGISTER_RETURN_CLASS, Block([]))
    defn.fullname = f"functools.{SINGLEDISPATCH_REGISTER_RETURN_CLASS}"
    info = TypeInfo(SymbolTable(), defn, "functools")
    obj_type = api.named_generic_type("builtins.object", []).type
    info.bases = [Instance(obj_type, [])]
    info.mro = [info, obj_type]
    defn.info = info

    func_arg = Argument(Var("name"), AnyType(TypeOfAny.implementation_artifact), None, ARG_POS)
    add_method_to_class(api, defn, "__call__", [func_arg], NoneType())

    return Instance(info, type_args)

