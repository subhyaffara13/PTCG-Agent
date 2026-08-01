
def analyze_member_access(
    name: str,
    typ: Type,
    context: Context,
    *,
    is_lvalue: bool,
    is_super: bool,
    is_operator: bool,
    original_type: Type,
    chk: TypeCheckerSharedApi,
    override_info: TypeInfo | None = None,
    in_literal_context: bool = False,
    self_type: Type | None = None,
    module_symbol_table: SymbolTable | None = None,
    no_deferral: bool = False,
    is_self: bool = False,
    rvalue: Expression | None = None,
    suppress_errors: bool = False,
) -> Type:
    """Return the type of attribute 'name' of 'typ'.

    The actual implementation is in '_analyze_member_access' and this docstring
    also applies to it.

    This is a general operation that supports various different variations:

      1. lvalue or non-lvalue access (setter or getter access)
      2. supertype access when using super() (is_super == True and
         'override_info' should refer to the supertype)

    'original_type' is the most precise inferred or declared type of the base object
    that we have available. When looking for an attribute of 'typ', we may perform
    recursive calls targeting the fallback type, and 'typ' may become some supertype
    of 'original_type'. 'original_type' is always preserved as the 'typ' type used in
    the initial, non-recursive call. The 'self_type' is a component of 'original_type'
    to which generic self should be bound (a narrower type that has a fallback to instance).
    Currently, this is used only for union types.

    'module_symbol_table' is passed to this function if 'typ' is actually a module,
    and we want to keep track of the available attributes of the module (since they
    are not available via the type object directly)

    'rvalue' can be provided optionally to infer better setter type when is_lvalue is True,
    most notably this helps for descriptors with overloaded __set__() method.

    'suppress_errors' will skip any logic that is only needed to generate error messages.
    Note that this more of a performance optimization, one should not rely on this to not
    show any messages, as some may be show e.g. by callbacks called here,
    use msg.filter_errors(), if needed.
    """
    mx = MemberContext(
        is_lvalue=is_lvalue,
        is_super=is_super,
        is_operator=is_operator,
        original_type=original_type,
        context=context,
        chk=chk,
        self_type=self_type,
        module_symbol_table=module_symbol_table,
        no_deferral=no_deferral,
        is_self=is_self,
        rvalue=rvalue,
        suppress_errors=suppress_errors,
    )
    result = _analyze_member_access(name, typ, mx, override_info)
    possible_literal = get_proper_type(result)
    if (
        in_literal_context
        and isinstance(possible_literal, Instance)
        and possible_literal.last_known_value is not None
    ):
        return possible_literal.last_known_value
    else:
        return result

