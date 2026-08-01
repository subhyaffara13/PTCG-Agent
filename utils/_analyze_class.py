
def _analyze_class(
    ctx: mypy.plugin.ClassDefContext, auto_attribs: bool | None, class_kw_only: bool
) -> list[Attribute]:
    """Analyze the class body of an attr maker, its parents, and return the Attributes found.

    auto_attribs=True means we'll generate attributes from type annotations also.
    auto_attribs=None means we'll detect which mode to use.
    class_kw_only=True means that all attributes created here will be keyword only args by
        default in __init__.
    """
    own_attrs: dict[str, Attribute] = {}
    if auto_attribs is None:
        auto_attribs = _detect_auto_attribs(ctx)

    # Walk the body looking for assignments and decorators.
    for stmt in ctx.cls.defs.body:
        if isinstance(stmt, AssignmentStmt):
            for attr in _attributes_from_assignment(ctx, stmt, auto_attribs, class_kw_only):
                # When attrs are defined twice in the same body we want to use the 2nd definition
                # in the 2nd location. So remove it from the OrderedDict.
                # Unless it's auto_attribs in which case we want the 2nd definition in the
                # 1st location.
                if not auto_attribs and attr.name in own_attrs:
                    del own_attrs[attr.name]
                own_attrs[attr.name] = attr
        elif isinstance(stmt, Decorator):
            _cleanup_decorator(stmt, own_attrs)

    for attribute in own_attrs.values():
        # Even though these look like class level assignments we want them to look like
        # instance level assignments.
        if attribute.name in ctx.cls.info.names:
            node = ctx.cls.info.names[attribute.name].node
            if isinstance(node, PlaceholderNode):
                # This node is not ready yet.
                continue
            assert isinstance(node, Var), node
            node.is_initialized_in_class = False

    # Traverse the MRO and collect attributes from the parents.
    taken_attr_names = set(own_attrs)
    super_attrs = []
    for super_info in ctx.cls.info.mro[1:-1]:
        if "attrs" in super_info.metadata:
            # Each class depends on the set of attributes in its attrs ancestors.
            ctx.api.add_plugin_dependency(make_wildcard_trigger(super_info.fullname))

            for data in super_info.metadata["attrs"]["attributes"]:
                # Only add an attribute if it hasn't been defined before.  This
                # allows for overwriting attribute definitions by subclassing.
                if data["name"] not in taken_attr_names:
                    a = Attribute.deserialize(super_info, data, ctx.api)
                    a.expand_typevar_from_subtype(ctx.cls.info)
                    super_attrs.append(a)
                    taken_attr_names.add(a.name)
    attributes = super_attrs + list(own_attrs.values())

    # Check the init args for correct default-ness.  Note: This has to be done after all the
    # attributes for all classes have been read, because subclasses can override parents.
    last_default = False

    for i, attribute in enumerate(attributes):
        if not attribute.init:
            continue

        if attribute.kw_only:
            # Keyword-only attributes don't care whether they are default or not.
            continue

        # If the issue comes from merging different classes, report it
        # at the class definition point.
        context = attribute.context if i >= len(super_attrs) else ctx.cls

        if not attribute.has_default and last_default:
            ctx.api.fail("Non-default attributes not allowed after default attributes.", context)
        last_default |= attribute.has_default

    return attributes


def _analyze_class(ctx: mypy.plugin.ClassDefContext) -> dict[str, _MethodInfo | None]:
    """Analyze the class body, its parents, and return the comparison methods found."""
    # Traverse the MRO and collect ordering methods.
    comparison_methods: dict[str, _MethodInfo | None] = {}
    # Skip object because total_ordering does not use methods from object
    for cls in ctx.cls.info.mro[:-1]:
        for name in _ORDERING_METHODS:
            if name in cls.names and name not in comparison_methods:
                node = cls.names[name].node
                if isinstance(node, SYMBOL_FUNCBASE_TYPES) and isinstance(node.type, CallableType):
                    comparison_methods[name] = _MethodInfo(node.is_static, node.type)
                    continue

                if isinstance(node, Var):
                    proper_type = get_proper_type(node.type)
                    if isinstance(proper_type, CallableType):
                        comparison_methods[name] = _MethodInfo(node.is_staticmethod, proper_type)
                        continue

                comparison_methods[name] = None

    return comparison_methods

