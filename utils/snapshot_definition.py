
def snapshot_definition(node: SymbolNode | None, common: SymbolSnapshot) -> SymbolSnapshot:
    """Create a snapshot description of a symbol table node.

    The representation is nested tuples and dicts. Only externally
    visible attributes are included.
    """
    if isinstance(node, SYMBOL_FUNCBASE_TYPES):
        # TODO: info
        if node.type:
            signature: tuple[object, ...] = snapshot_type(node.type)
        else:
            signature = snapshot_untyped_signature(node)
        impl: FuncDef | None = None
        if isinstance(node, FuncDef):
            impl = node
        elif node.impl:
            impl = node.impl.func if isinstance(node.impl, Decorator) else node.impl
        setter_type = None
        if isinstance(node, OverloadedFuncDef) and node.items:
            first_item = node.items[0]
            if isinstance(first_item, Decorator) and first_item.func.is_property:
                setter_type = snapshot_optional_type(first_item.var.setter_type)
        is_trivial_body = impl.is_trivial_body if impl else False
        dataclass_transform_spec = find_dataclass_transform_spec(node)

        deprecated: str | list[str | None] | None = None
        if isinstance(node, FuncDef):
            deprecated = node.deprecated
        elif isinstance(node, OverloadedFuncDef):
            deprecated = [node.deprecated] + [
                i.func.deprecated for i in node.items if isinstance(i, Decorator)
            ]

        return (
            "Func",
            common,
            node.is_property,
            node.is_final,
            node.is_class,
            node.is_static,
            signature,
            is_trivial_body,
            dataclass_transform_spec.serialize() if dataclass_transform_spec is not None else None,
            deprecated,
            setter_type,  # multi-part properties are stored as OverloadedFuncDef
        )
    elif isinstance(node, Var):
        return ("Var", common, snapshot_optional_type(node.type), node.is_final)
    elif isinstance(node, Decorator):
        # Note that decorated methods are represented by Decorator instances in
        # a symbol table since we need to preserve information about the
        # decorated function (whether it's a class function, for
        # example). Top-level decorated functions, however, are represented by
        # the corresponding Var node, since that happens to provide enough
        # context.
        return (
            "Decorator",
            node.is_overload,
            snapshot_optional_type(node.var.type),
            snapshot_definition(node.func, common),
        )
    elif isinstance(node, TypeInfo):
        dataclass_transform_spec = node.dataclass_transform_spec
        if dataclass_transform_spec is None:
            dataclass_transform_spec = find_dataclass_transform_spec(node)

        attrs = (
            node.is_abstract,
            node.is_enum,
            node.is_protocol,
            node.fallback_to_any,
            node.meta_fallback_to_any,
            node.is_named_tuple,
            node.is_newtype,
            # We need this to e.g. trigger metaclass calculation in subclasses.
            snapshot_optional_type(node.metaclass_type),
            snapshot_optional_type(node.tuple_type),
            snapshot_optional_type(node.typeddict_type),
            [base.fullname for base in node.mro],
            # Note that the structure of type variables is a part of the external interface,
            # since creating instances might fail, for example:
            #     T = TypeVar('T', bound=int)
            #     class C(Generic[T]):
            #         ...
            #     x: C[str] <- this is invalid, and needs to be re-checked if `T` changes.
            # An alternative would be to create both deps: <...> -> C, and <...> -> <C>,
            # but this currently seems a bit ad hoc.
            tuple(snapshot_type(tdef) for tdef in node.defn.type_vars),
            [snapshot_type(base) for base in node.bases],
            [snapshot_type(p) for p in node._promote],
            dataclass_transform_spec.serialize() if dataclass_transform_spec is not None else None,
            node.deprecated,
        )
        prefix = node.fullname
        symbol_table = snapshot_symbol_table(prefix, node.names)
        # Special dependency for abstract attribute handling.
        symbol_table["(abstract)"] = ("Abstract", tuple(sorted(node.abstract_attributes)))
        return ("TypeInfo", common, attrs, symbol_table)
    else:
        # Other node types are handled elsewhere.
        assert False, type(node)

