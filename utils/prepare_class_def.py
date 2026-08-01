
def prepare_class_def(
    path: str,
    module_name: str,
    cdef: ClassDef,
    errors: Errors,
    mapper: Mapper,
    options: CompilerOptions,
) -> None:
    """Populate the interface-level information in a class IR.

    This includes attribute and method declarations, and the MRO, among other things, but
    method bodies are generated in a later pass.
    """

    ir = mapper.type_to_ir[cdef.info]
    info = cdef.info

    attrs, attrs_lines = get_mypyc_attrs(cdef, path, errors)
    if attrs.get("allow_interpreted_subclasses") is True:
        ir.allow_interpreted_subclasses = True
    if attrs.get("serializable") is True:
        # Supports copy.copy and pickle (including subclasses)
        ir._serializable = True

    if attrs.get("acyclic") is True:
        ir.is_acyclic = True

    # Check for subclassing from builtin types
    for cls in info.mro:
        # Special case exceptions and dicts
        # XXX: How do we handle *other* things??
        if cls.fullname == "builtins.BaseException":
            ir.builtin_base = "PyBaseExceptionObject"
        elif cls.fullname == "builtins.dict":
            ir.builtin_base = "PyDictObject"
        elif cls.fullname.startswith("builtins."):
            if not can_subclass_builtin(cls.fullname):
                # Note that if we try to subclass a C extension class that
                # isn't in builtins, bad things will happen and we won't
                # catch it here! But this should catch a lot of the most
                # common pitfalls.
                errors.error(
                    "Inheriting from most builtin types is unimplemented", path, cdef.line
                )
                errors.note(
                    "Potential workaround: @mypy_extensions.mypyc_attr(native_class=False)",
                    path,
                    cdef.line,
                )
                errors.note(
                    "https://mypyc.readthedocs.io/en/stable/native_classes.html#defining-non-native-classes",
                    path,
                    cdef.line,
                )

    free_list_len = attrs.get("free_list_len")
    if free_list_len is not None:
        line = attrs_lines["free_list_len"]
        if ir.is_trait:
            errors.error('"free_list_len" can\'t be used with traits', path, line)
        if ir.allow_interpreted_subclasses:
            errors.error(
                '"free_list_len" can\'t be used in a class that allows interpreted subclasses',
                path,
                line,
            )
        if ir.builtin_base:
            errors.error(
                '"free_list_len" can\'t be used in a class that inherits from a built-in type',
                path,
                line,
            )
        if free_list_len == 1:
            ir.reuse_freed_instance = True
        else:
            errors.error(f'Unsupported value for "free_list_len": {free_list_len}', path, line)

    # Set up the parent class
    bases = [mapper.type_to_ir[base.type] for base in info.bases if base.type in mapper.type_to_ir]
    if len(bases) > 1 and any(not c.is_trait for c in bases) and bases[0].is_trait:
        # If the first base is a non-trait, don't ever error here. While it is correct
        # to error if a trait comes before the next non-trait base (e.g. non-trait, trait,
        # non-trait), it's pointless, confusing noise from the bigger issue: multiple
        # inheritance is *not* supported.
        errors.error("Non-trait base must appear first in parent list", path, cdef.line)
    ir.traits = [c for c in bases if c.is_trait]

    mro = []  # All mypyc base classes
    base_mro = []  # Non-trait mypyc base classes
    for cls in info.mro:
        if cls not in mapper.type_to_ir:
            if cls.fullname != "builtins.object":
                ir.inherits_python = True
            continue
        base_ir = mapper.type_to_ir[cls]
        if not base_ir.is_trait:
            base_mro.append(base_ir)
        mro.append(base_ir)

        if cls.defn.removed_base_type_exprs or not base_ir.is_ext_class:
            ir.inherits_python = True

    base_idx = 1 if not ir.is_trait else 0
    if len(base_mro) > base_idx:
        ir.base = base_mro[base_idx]
    ir.mro = mro
    ir.base_mro = base_mro

    prepare_methods_and_attributes(cdef, ir, path, module_name, errors, mapper, options)
    prepare_init_method(cdef, ir, module_name, mapper)

    for base in bases:
        if base.children is not None:
            base.children.append(ir)

    if is_dataclass(cdef):
        ir.is_augmented = True

