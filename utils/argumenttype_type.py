
def argumenttype_type(
    t: Type,
    *,
    mutable: bool,
    binds: ArgName,
    remove_non_owning_ref_types: bool = False,
    symint: bool = False,
) -> NamedCType:
    # If it's a value type, do the value type translation
    r = valuetype_type(
        t,
        binds=binds,
        mutable=mutable,
        symint=symint,
    )
    if r is not None:
        return r

    if isinstance(t, BaseType):
        if t.name == BaseTy.Tensor:
            if mutable and not local.use_const_ref_for_mutable_tensors():
                return NamedCType(binds, MutRefCType(BaseCType(tensorT)))
            else:
                return NamedCType(binds, ConstRefCType(BaseCType(tensorT)))
        elif t.name == BaseTy.Scalar:
            return NamedCType(binds, ConstRefCType(BaseCType(scalarT)))
        else:
            raise AssertionError(f"base type should have been value type {t}")
    elif isinstance(t, OptionalType):
        if str(t.elem) == "Tensor":
            if mutable and not local.use_const_ref_for_mutable_tensors():
                return NamedCType(
                    binds, MutRefCType(BaseCType(tensorT))
                )  # TODO: fix this discrepancy
            else:
                return NamedCType(
                    binds, ConstRefCType(OptionalCType(BaseCType(tensorT)))
                )
        elif str(t.elem) == "Scalar":
            return NamedCType(binds, ConstRefCType(OptionalCType(BaseCType(scalarT))))
        elif isinstance(t.elem, ListType) and str(t.elem.elem) == "int":
            return NamedCType(binds, BaseCType(optionalIntArrayRefT))
        elif isinstance(t.elem, ListType) and str(t.elem.elem) == "SymInt":
            if symint:
                return NamedCType(binds, BaseCType(optionalSymIntArrayRefT))
            else:
                return NamedCType(binds, BaseCType(optionalIntArrayRefT))
        elem = argumenttype_type(t.elem, mutable=mutable, binds=binds, symint=symint)
        return NamedCType(binds, OptionalCType(elem.type))
    elif isinstance(t, ListType):
        # TODO: remove these special cases, ArrayRef fallthrough works fine
        if str(t.elem) == "int":
            if remove_non_owning_ref_types:
                return NamedCType(binds, VectorCType(BaseCType(longT)))
            else:
                return NamedCType(binds, BaseCType(intArrayRefT))
        if str(t.elem) == "SymInt":
            if remove_non_owning_ref_types:
                if symint:
                    return NamedCType(binds, VectorCType(BaseCType(SymIntT)))
                else:
                    return NamedCType(binds, VectorCType(BaseCType(longT)))
            else:
                if symint:
                    return NamedCType(binds, BaseCType(symIntArrayRefT))
                else:
                    return NamedCType(binds, BaseCType(intArrayRefT))
        if str(t.elem) == "Tensor":
            if local.use_ilistref_for_tensor_lists():
                return NamedCType(binds, ConstRefCType(BaseCType(iTensorListRefT)))
            else:
                return NamedCType(binds, BaseCType(tensorListT))
        elif str(t.elem) == "Scalar":
            return NamedCType(binds, ArrayRefCType(BaseCType(scalarT)))
        elif str(t.elem) == "Dimname":
            return NamedCType(binds, BaseCType(dimnameListT))
        elif str(t.elem) == "Tensor?":
            return NamedCType(
                binds, ConstRefCType(ListCType(OptionalCType(BaseCType(tensorT))))
            )
        elem = argumenttype_type(t.elem, mutable=mutable, binds=binds, symint=symint)
        return NamedCType(binds, ArrayRefCType(elem.type))
    else:
        raise AssertionError(f"unrecognized type {repr(t)}")


def argumenttype_type(
    t: Type,
    *,
    mutable: bool,
    binds: ArgName,
    remove_non_owning_ref_types: bool = False,
    symint: bool = True,
) -> NamedCType:
    # This is a faux amis.  If it makes sense in the future to add
    # more special cases here, or invert things so cpp.argument_type
    # calls this, or just completely inline the function, please do
    # it.
    return cpp.argumenttype_type(
        t,
        mutable=mutable,
        binds=binds,
        symint=symint,
        remove_non_owning_ref_types=remove_non_owning_ref_types,
    )


def argumenttype_type(
    t: Type, *, mutable: bool, binds: ArgName, symint: bool
) -> NamedCType:
    if str(t) == "Tensor?":
        tensor_type: OptionalCType = OptionalCType(BaseCType(tensorT))
        if mutable and not local.use_const_ref_for_mutable_tensors():
            return NamedCType(binds, MutRefCType(tensor_type))
        else:
            return NamedCType(binds, ConstRefCType(tensor_type))
    elif str(t) == "Tensor?[]":
        return NamedCType(
            binds, ConstRefCType(ListCType(OptionalCType(BaseCType(tensorT))))
        )
    elif str(t) == "Scalar":
        return NamedCType(binds, ConstRefCType(BaseCType(scalarT)))
    elif str(t) == "Scalar?":
        return NamedCType(binds, ConstRefCType(OptionalCType(BaseCType(scalarT))))
    return cpp.argumenttype_type(t, mutable=mutable, binds=binds, symint=symint)


def argumenttype_type(t: Type, *, mutable: bool, binds: ArgName) -> NamedCType:
    # If it's a value type, do the value type translation
    # NB: structured kernels ALWAYS have symint off, since they involve actual
    # kernels that require real ints.  The one exception is the
    # CompositeExplicitAutograd and the meta function (which could
    # hypothetically be SymInt), but for simplicity we plan for these to just
    # be handled in Python
    r = cpp.valuetype_type(t, symint=False, binds=binds, mutable=mutable)
    if r is not None:
        return r

    if isinstance(t, BaseType):
        if t.name == BaseTy.Tensor:
            return NamedCType(binds, ConstRefCType(BaseCType(tensorT)))
        elif t.name == BaseTy.Scalar:
            return NamedCType(binds, ConstRefCType(BaseCType(scalarT)))
        else:
            raise AssertionError(f"base type should have been value type {t}")
    elif isinstance(t, OptionalType):
        if t.elem == BaseType(BaseTy.Tensor):
            return NamedCType(binds, BaseCType(optionalTensorRefT))
        elif t.elem == BaseType(BaseTy.Scalar):
            return NamedCType(binds, BaseCType(optionalScalarRefT))
        elif isinstance(t.elem, ListType) and str(t.elem.elem) == "int":
            return NamedCType(binds, BaseCType(optionalIntArrayRefT))
        elem = argumenttype_type(t.elem, mutable=mutable, binds=binds)
        return NamedCType(binds, OptionalCType(elem.type))
    elif isinstance(t, ListType):
        if t.elem == BaseType(BaseTy.Tensor):
            return NamedCType(binds, ConstRefCType(BaseCType(iTensorListRefT)))
        elif t.elem == OptionalType(BaseType(BaseTy.Tensor)):
            return NamedCType(binds, BaseCType(iOptTensorListRefT))
        # TODO: delete these special cases; see torchgen.api.cpp--these
        # must be changed in tandem, but there are problems; see
        # https://github.com/pytorch/pytorch/pull/51485
        elif str(t.elem) == "int":
            return NamedCType(binds, BaseCType(intArrayRefT))
        elif str(t.elem) == "Dimname":
            return NamedCType(binds, BaseCType(dimnameListT))
        elem = argumenttype_type(t.elem, mutable=mutable, binds=binds)
        return NamedCType(binds, ArrayRefCType(elem.type))
    else:
        raise AssertionError(f"unrecognized type {repr(t)}")

