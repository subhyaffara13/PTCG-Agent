
def is_wrapper_or_member_descriptor(
    value: Any,
) -> TypeIs[
    types.GetSetDescriptorType
    | types.MethodDescriptorType
    | types.WrapperDescriptorType
    | types.MemberDescriptorType
    | types.MethodWrapperType
]:
    return isinstance(
        value,
        (
            # set up by PyGetSetDef
            types.GetSetDescriptorType,
            # set by PyMethodDef, e.g. list.append
            types.MethodDescriptorType,
            # slots - list.__add__
            types.WrapperDescriptorType,
            # set up by PyMemberDef
            types.MemberDescriptorType,
            # wrapper over C functions
            types.MethodWrapperType,
        ),
    )

