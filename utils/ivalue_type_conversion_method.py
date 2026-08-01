
def ivalue_type_conversion_method(
    arg_type: BaseType | OptionalType | Type,
) -> tuple[bool, str] | None:
    """
    Return the method call expression of `c10::ivalue' to convert its contained value to
    the expected value of `arg_type` type. For example, for `arg_type` == BaseTy.Tensor,
    this function returns ".toTensor()", so that it can be appended to the ivalue's
    variable name to get the value of the expected type.
    """
    type_conversion_methods = {
        BaseTy.Tensor: ((True, "toTensor()"), (False, "toOptional<at::Tensor>()")),
        BaseTy.int: ((False, "toInt()"), (False, "toOptional<int64_t>()")),
        BaseTy.bool: ((False, "toBool()"), (False, "toOptional<bool>()")),
        BaseTy.Scalar: ((False, "toScalar()"), (False, "toOptional<at::Scalar>()")),
        BaseTy.ScalarType: (
            (False, "toScalarType()"),
            (False, "toOptional<at::ScalarType>()"),
        ),
        BaseTy.str: (
            (False, "toStringView()"),
            (False, "toOptional<c10::string_view>()"),
            (False, "toOptional<::std::string_view>()"),
        ),
    }

    base_ty_object = None
    if isinstance(arg_type, BaseType):
        base_ty_object = arg_type.name
    elif isinstance(arg_type, OptionalType):
        if not isinstance(arg_type.elem, BaseType):
            # ListType is currently unsupported.
            return None
        base_ty_object = arg_type.elem.name
    else:
        return None

    if base_ty_object not in type_conversion_methods:
        return None
    methods = type_conversion_methods[base_ty_object]
    if isinstance(arg_type, BaseType):
        return methods[0]
    return methods[1]

