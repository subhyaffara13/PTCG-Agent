
def add_attribute_to_class(
    api: SemanticAnalyzerPluginInterface,
    cls: ClassDef,
    name: str,
    typ: Type,
    final: bool = False,
    no_serialize: bool = False,
    override_allow_incompatible: bool = False,
    fullname: str | None = None,
    is_classvar: bool = False,
    overwrite_existing: bool = False,
) -> Var:
    """
    Adds a new attribute to a class definition.
    This currently only generates the symbol table entry and no corresponding AssignmentStatement
    """
    info = cls.info

    # NOTE: we would like the plugin generated node to dominate, but we still
    # need to keep any existing definitions so they get semantically analyzed.
    if name in info.names and not overwrite_existing:
        # Get a nice unique name instead.
        r_name = get_unique_redefinition_name(name, info.names)
        info.names[r_name] = info.names[name]

    node = Var(name, typ)
    node.info = info
    node.is_final = final
    node.is_classvar = is_classvar
    if name in ALLOW_INCOMPATIBLE_OVERRIDE:
        node.allow_incompatible_override = True
    else:
        node.allow_incompatible_override = override_allow_incompatible

    if fullname:
        node._fullname = fullname
    else:
        node._fullname = info.fullname + "." + name

    info.names[name] = SymbolTableNode(
        MDEF, node, plugin_generated=True, no_serialize=no_serialize
    )
    return node

