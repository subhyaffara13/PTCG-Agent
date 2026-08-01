
def is_valid_inferred_type(
    typ: Type, options: Options, is_lvalue_final: bool = False, is_lvalue_member: bool = False
) -> bool:
    """Is an inferred type valid and needs no further refinement?

    Examples of invalid types include the None type (when we are not assigning
    None to a final lvalue) or List[<uninhabited>].

    When not doing strict Optional checking, all types containing None are
    invalid.  When doing strict Optional checking, only None and types that are
    incompletely defined (i.e. contain UninhabitedType) are invalid.
    """
    proper_type = get_proper_type(typ)
    if isinstance(proper_type, NoneType):
        # If the lvalue is final, we may immediately infer NoneType when the
        # initializer is None.
        #
        # If not, we want to defer making this decision. The final inferred
        # type could either be NoneType or an Optional type, depending on
        # the context. This resolution happens in leave_partial_types when
        # we pop a partial types scope.
        return is_lvalue_final or (not is_lvalue_member and options.allow_redefinition)
    elif isinstance(proper_type, UninhabitedType):
        return False
    return not typ.accept(InvalidInferredTypes())

