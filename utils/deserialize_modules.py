
def deserialize_modules(data: dict[str, JsonDict], ctx: DeserMaps) -> dict[str, ModuleIR]:
    """Deserialize a collection of modules.

    The modules can contain dependencies on each other.

    Arguments:
        data: A dict containing the modules to deserialize.
        ctx: The deserialization maps to use and to populate.
             They are populated with information from the deserialized
             modules and as a precondition must have been populated by
             deserializing any dependencies of the modules being deserialized
             (outside of dependencies between the modules themselves).

    Returns a map containing the deserialized modules.
    """
    for mod in data.values():
        # First create ClassIRs for every class so that we can construct types and whatnot
        for cls in mod["classes"]:
            ir = ClassIR(cls["name"], cls["module_name"])
            assert ir.fullname not in ctx.classes, "Class %s already in map" % ir.fullname
            ctx.classes[ir.fullname] = ir

    for mod in data.values():
        # Then deserialize all of the functions so that methods are available
        # to the class deserialization.
        for method in mod["functions"]:
            func = FuncIR.deserialize(method, ctx)
            assert func.decl.id not in ctx.functions, (
                "Method %s already in map" % func.decl.fullname
            )
            ctx.functions[func.decl.id] = func

    return {k: ModuleIR.deserialize(v, ctx) for k, v in data.items()}

