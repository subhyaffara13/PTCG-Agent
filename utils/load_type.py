
def load_type(builder: IRBuilder, typ: TypeInfo, unbounded_type: Type | None, line: int) -> Value:
    # typ.fullname contains the module where the class object was defined. However, it is possible
    # that the class object's module was not imported in the file currently being compiled. So, we
    # use unbounded_type.name (if provided by caller) to load the class object through one of the
    # imported modules.
    # Example: for `json.JSONDecoder`, typ.fullname is `json.decoder.JSONDecoder` but the Python
    # file may import `json` not `json.decoder`.
    # Another corner case: The Python file being compiled imports mod1 and has a type hint
    # `mod1.OuterClass.InnerClass`. But, mod1/__init__.py might import OuterClass like this:
    # `from mod2.mod3 import OuterClass`. In this case, typ.fullname is
    # `mod2.mod3.OuterClass.InnerClass` and `unbounded_type.name` is `mod1.OuterClass.InnerClass`.
    # So, we must use unbounded_type.name to load the class object.
    # See issue mypyc/mypyc#1087.
    if typ in builder.mapper.type_to_ir:
        class_ir = builder.mapper.type_to_ir[typ]
        class_obj = builder.builder.get_native_type(class_ir)
    elif builtin := builder.load_builtin(typ.fullname, line):
        class_obj = builtin
    elif isinstance(unbounded_type, UnboundType):
        path_parts = unbounded_type.name.split(".")
        class_obj = builder.load_global_str(path_parts[0], line)
        for attr in path_parts[1:]:
            class_obj = builder.py_get_attr(class_obj, attr, line)
    else:
        class_obj = builder.load_global_str(typ.name, line)

    return class_obj

