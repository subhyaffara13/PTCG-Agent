
def populate_non_ext_bases(builder: IRBuilder, cdef: ClassDef) -> Value:
    """Create base class tuple of a non-extension class.

    The tuple is passed to the metaclass constructor.
    """
    is_named_tuple = cdef.info.is_named_tuple
    ir = builder.mapper.type_to_ir[cdef.info]
    bases = []
    for cls in (b.type for b in cdef.info.bases):
        if cls.fullname == "builtins.object":
            continue
        if is_named_tuple and cls.fullname in (
            "typing.Sequence",
            "typing.Iterable",
            "typing.Collection",
            "typing.Reversible",
            "typing.Container",
            "typing.Sized",
        ):
            # HAX: Synthesized base classes added by mypy don't exist at runtime, so skip them.
            #      This could break if they were added explicitly, though...
            continue
        # Add the current class to the base classes list of concrete subclasses
        if cls in builder.mapper.type_to_ir:
            base_ir = builder.mapper.type_to_ir[cls]
            if base_ir.children is not None:
                base_ir.children.append(ir)

        if cls.fullname in MAGIC_TYPED_DICT_CLASSES:
            # HAX: Mypy internally represents TypedDict classes differently from what
            #      should happen at runtime. Replace with something that works.
            module = "typing"
            name = "_TypedDict"
            base = builder.get_module_attr(module, name, cdef.line)
        elif is_named_tuple and cls.fullname == "builtins.tuple":
            name = "_NamedTuple"
            base = builder.get_module_attr("typing", name, cdef.line)
        else:
            cls_module = cls.fullname.rsplit(".", 1)[0]
            if cls_module == builder.current_module:
                base = builder.load_global_str(cls.name, cdef.line)
            else:
                base = builder.load_module_attr_by_fullname(cls.fullname, cdef.line)
        bases.append(base)
        if cls.fullname in MAGIC_TYPED_DICT_CLASSES:
            # The remaining base classes are synthesized by mypy and should be ignored.
            break
    return builder.new_tuple(bases, cdef.line)

