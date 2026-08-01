
def calculate_class_abstract_status(typ: TypeInfo, is_stub_file: bool, errors: Errors) -> None:
    """Calculate abstract status of a class.

    Set is_abstract of the type to True if the type has an unimplemented
    abstract attribute.  Also compute a list of abstract attributes.
    Report error is required ABCMeta metaclass is missing.
    """
    typ.is_abstract = False
    typ.abstract_attributes = []
    if typ.typeddict_type:
        return  # TypedDict can't be abstract
    concrete: set[str] = set()
    # List of abstract attributes together with their abstract status
    abstract: list[tuple[str, int]] = []
    abstract_in_this_class: list[str] = []
    if typ.is_newtype:
        # Special case: NewTypes are considered as always non-abstract, so they can be used as:
        #     Config = NewType('Config', Mapping[str, str])
        #     default = Config({'cannot': 'modify'})  # OK
        return
    for base in typ.mro:
        for name, symnode in base.names.items():
            node = symnode.node
            if isinstance(node, OverloadedFuncDef):
                # Unwrap an overloaded function definition. We can just
                # check arbitrarily the first overload item. If the
                # different items have a different abstract status, there
                # should be an error reported elsewhere.
                if node.items:  # can be empty for invalid overloads
                    func: Node | None = node.items[0]
                else:
                    func = None
            else:
                func = node
            if isinstance(func, Decorator):
                func = func.func
            if isinstance(func, FuncDef):
                if (
                    func.abstract_status in (IS_ABSTRACT, IMPLICITLY_ABSTRACT)
                    and name not in concrete
                ):
                    typ.is_abstract = True
                    abstract.append((name, func.abstract_status))
                    if base is typ:
                        abstract_in_this_class.append(name)
            elif isinstance(node, Var):
                if node.is_abstract_var and name not in concrete:
                    typ.is_abstract = True
                    abstract.append((name, IS_ABSTRACT))
                    if base is typ:
                        abstract_in_this_class.append(name)
            concrete.add(name)
    # In stubs, abstract classes need to be explicitly marked because it is too
    # easy to accidentally leave a concrete class abstract by forgetting to
    # implement some methods.
    typ.abstract_attributes = sorted(abstract)
    if is_stub_file:
        if typ.declared_metaclass and typ.declared_metaclass.type.has_base("abc.ABCMeta"):
            return
        if typ.is_protocol:
            return
        if abstract and not abstract_in_this_class:

            def report(message: str, severity: str) -> None:
                errors.report(typ.line, typ.column, message, severity=severity)

            attrs = ", ".join(f'"{attr}"' for attr, _ in sorted(abstract))
            report(f"Class {typ.fullname} has abstract attributes {attrs}", "error")
            report(
                "If it is meant to be abstract, add 'abc.ABCMeta' as an explicit metaclass", "note"
            )
    if typ.is_final and abstract:
        attrs = ", ".join(f'"{attr}"' for attr, _ in sorted(abstract))
        errors.report(
            typ.line, typ.column, f"Final class {typ.fullname} has abstract attributes {attrs}"
        )

