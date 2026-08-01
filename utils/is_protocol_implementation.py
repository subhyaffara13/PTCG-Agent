
def is_protocol_implementation(
    left: Instance | TupleType,
    right: Instance,
    proper_subtype: bool = False,
    class_obj: bool = False,
    skip: list[str] | None = None,
    options: Options | None = None,
) -> bool:
    """Check whether 'left' implements the protocol 'right'.

    If 'proper_subtype' is True, then check for a proper subtype.
    Treat recursive protocols by using the 'assuming' structural subtype matrix
    (in sparse representation, i.e. as a list of pairs (subtype, supertype)),
    see also comment in nodes.TypeInfo. When we enter a check for classes
    (A, P), defined as following::

      class P(Protocol):
          def f(self) -> P: ...
      class A:
          def f(self) -> A: ...

    this results in A being a subtype of P without infinite recursion.
    On every false result, we pop the assumption, thus avoiding an infinite recursion
    as well.
    """
    assert right.type.is_protocol
    if skip is None:
        skip = []
    # Preserve original left type for precise self-type binding. Only tuple types are
    # supported for now.
    original_left = left
    if isinstance(left, TupleType):
        left = mypy.typeops.tuple_fallback(left)
    # We need to record this check to generate protocol fine-grained dependencies.
    type_state.record_protocol_subtype_check(left.type, right.type)
    # nominal subtyping currently ignores '__init__' and '__new__' signatures
    members_not_to_check = {"__init__", "__new__"}
    members_not_to_check.update(skip)
    # Trivial check that circumvents the bug described in issue 9771:
    if left.type.is_protocol:
        members_right = set(right.type.protocol_members) - members_not_to_check
        members_left = set(left.type.protocol_members) - members_not_to_check
        if not members_right.issubset(members_left):
            return False
    assuming = right.type.assuming_proper if proper_subtype else right.type.assuming
    for l, r in reversed(assuming):
        if l == left and r == right:
            return True
    with pop_on_exit(assuming, left, right):
        for member in right.type.protocol_members:
            if member in members_not_to_check:
                continue
            ignore_names = member != "__call__"  # __call__ can be passed kwargs
            # The third argument below indicates to what self type is bound.
            # We always bind self to the subtype. (Similarly to nominal types).
            supertype = find_member(member, right, original_left)
            assert supertype is not None

            subtype = get_protocol_member(left, original_left, member, class_obj)
            # Useful for debugging:
            # print(member, 'of', left, 'has type', subtype)
            # print(member, 'of', right, 'has type', supertype)
            if not subtype:
                return False
            if not proper_subtype:
                # Nominal check currently ignores arg names
                # NOTE: If we ever change this, be sure to also change the call to
                # SubtypeVisitor.build_subtype_kind(...) down below.
                is_compat = is_subtype(
                    subtype, supertype, ignore_pos_arg_names=ignore_names, options=options
                )
            else:
                is_compat = is_proper_subtype(subtype, supertype)
            if not is_compat:
                return False
            if isinstance(get_proper_type(subtype), NoneType) and isinstance(
                get_proper_type(supertype), CallableType
            ):
                # We want __hash__ = None idiom to work even without --strict-optional
                return False
            subflags = get_member_flags(member, left, class_obj=class_obj)
            superflags = get_member_flags(member, right)
            if IS_SETTABLE in superflags:
                # Check opposite direction for settable attributes.
                if IS_EXPLICIT_SETTER in superflags:
                    supertype = find_member(member, right, original_left, is_lvalue=True)
                if IS_EXPLICIT_SETTER in subflags:
                    subtype = get_protocol_member(
                        left, original_left, member, class_obj, is_lvalue=True
                    )
                # At this point we know attribute is present on subtype, otherwise we
                # would return False above.
                assert supertype is not None and subtype is not None
                if not is_subtype(supertype, subtype, options=options):
                    return False
            if IS_SETTABLE in superflags and IS_SETTABLE not in subflags:
                return False
            if not class_obj:
                if IS_SETTABLE not in superflags:
                    if IS_CLASSVAR in superflags and IS_CLASSVAR not in subflags:
                        return False
                elif (IS_CLASSVAR in subflags) != (IS_CLASSVAR in superflags):
                    return False
            else:
                if IS_VAR in superflags and IS_CLASSVAR not in subflags:
                    # Only class variables are allowed for class object access.
                    return False
                if IS_CLASSVAR in superflags:
                    # This can be never matched by a class object.
                    return False
            # This rule is copied from nominal check in checker.py
            if IS_CLASS_OR_STATIC in superflags and IS_CLASS_OR_STATIC not in subflags:
                return False

    if not proper_subtype:
        # Nominal check currently ignores arg names, but __call__ is special for protocols
        ignore_names = right.type.protocol_members != ["__call__"]
    else:
        ignore_names = False
    subtype_kind = SubtypeVisitor.build_subtype_kind(
        subtype_context=SubtypeContext(ignore_pos_arg_names=ignore_names),
        proper_subtype=proper_subtype,
    )
    type_state.record_subtype_cache_entry(subtype_kind, left, right)
    return True

