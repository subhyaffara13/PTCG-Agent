
def _emit_no_member(
    node: nodes.Attribute | nodes.AssignAttr | nodes.DelAttr,
    owner: InferenceResult,
    owner_name: str | None,
    mixin_class_rgx: Pattern[str],
    ignored_mixins: bool = True,
    ignored_none: bool = True,
) -> bool:
    """Try to see if no-member should be emitted for the given owner.

    The following cases are ignored:

        * the owner is a function and it has decorators.
        * the owner is an instance and it has __getattr__, __getattribute__ implemented
        * the module is explicitly ignored from no-member checks
        * the owner is a class and the name can be found in its metaclass.
        * The access node is protected by an except handler, which handles
          AttributeError, Exception or bare except.
        * The node is guarded behind and `IF` or `IFExp` node
    """
    # pylint: disable = too-many-return-statements
    if node_ignores_exception(node, AttributeError):
        return False
    if ignored_none and isinstance(owner, nodes.Const) and owner.value is None:
        return False
    if is_super(owner) or getattr(owner, "type", None) == "metaclass":
        return False
    if owner_name and ignored_mixins and mixin_class_rgx.match(owner_name):
        return False
    if isinstance(owner, nodes.FunctionDef) and (
        owner.decorators or owner.is_abstract()
    ):
        return False
    if isinstance(owner, (astroid.Instance, nodes.ClassDef)):
        # Issue #2565: Don't ignore enums, as they have a `__getattr__` but it's not
        # invoked at this point.
        if _is_enum_owner(owner):
            return not _enum_has_attribute(owner, node)
        # Note: non-enum owners with a dynamic ``__getattr__`` are handled
        # earlier, in ``visit_attribute``, where the whole check is skipped.
        if not has_known_bases(owner):
            return False

        # Exclude typed annotations, since these might actually exist
        # at some point during the runtime of the program.
        if utils.is_attribute_typed_annotation(owner, node.attrname):
            return False
    if isinstance(owner, objects.Super):
        # Verify if we are dealing with an invalid Super object.
        # If it is invalid, then there's no point in checking that
        # it has the required attribute. Also, don't fail if the
        # MRO is invalid.
        try:
            owner.super_mro()
        except (astroid.MroError, astroid.SuperError):
            return False
        if not all(has_known_bases(base) for base in owner.type.mro()):
            return False
    if isinstance(owner, nodes.Module):
        try:
            owner.getattr("__getattr__")
            return False
        except astroid.NotFoundError:
            pass
    if owner_name and node.attrname.startswith("_" + owner_name):
        # Test if an attribute has been mangled ('private' attribute)
        unmangled_name = node.attrname.split("_" + owner_name)[-1]
        try:
            if owner.getattr(unmangled_name, context=None) is not None:
                return False
        except astroid.NotFoundError:
            return True

    # Don't emit no-member if guarded behind `IF` or `IFExp`
    #   * Walk up recursively until if statement is found.
    #   * Check if condition can be inferred as `Const`,
    #       would evaluate as `False`,
    #       and whether the node is part of the `body`.
    #   * Continue checking until scope of node is reached.
    scope: nodes.NodeNG = node.scope()
    node_origin: nodes.NodeNG = node
    parent: nodes.NodeNG = node.parent
    while parent != scope:
        if isinstance(parent, (nodes.If, nodes.IfExp)):
            inferred = safe_infer(parent.test)
            if (  # pylint: disable=too-many-boolean-expressions
                isinstance(inferred, nodes.Const)
                and inferred.bool_value() is False
                and (
                    (isinstance(parent, nodes.If) and node_origin in parent.body)
                    or (isinstance(parent, nodes.IfExp) and node_origin == parent.body)
                )
            ):
                return False
        node_origin, parent = parent, parent.parent

    return True

