
def infer_variance(info: TypeInfo, i: int) -> bool:
    """Infer the variance of the ith type variable of a generic class.

    Return True if successful. This can fail if some inferred types aren't ready.
    """
    object_type = Instance(info.mro[-1], [])

    for variance in COVARIANT, CONTRAVARIANT, INVARIANT:
        tv = info.defn.type_vars[i]
        assert isinstance(tv, TypeVarType)
        if tv.variance != VARIANCE_NOT_READY:
            continue
        tv.variance = variance
        co = True
        contra = True
        tvar = info.defn.type_vars[i]
        self_type = fill_typevars(info)
        for member in all_non_object_members(info):
            # __mypy-replace is an implementation detail of the dataclass plugin
            if member in {"__init__", "__new__", "__replace__", "__mypy-replace"}:
                continue

            if isinstance(self_type, TupleType):
                self_type = mypy.typeops.tuple_fallback(self_type)
            flags = get_member_flags(member, self_type)
            settable = IS_SETTABLE in flags

            node = info[member].node
            if isinstance(node, Var):
                if node.type is None:
                    tv.variance = VARIANCE_NOT_READY
                    return False
                if has_underscore_prefix(member):
                    # Special case to avoid false positives (and to pass conformance tests)
                    settable = False

            # TODO: handle settable properties with setter type different from getter.
            typ = find_member(member, self_type, self_type)
            if typ:
                # It's okay for a method in a generic class with a contravariant type
                # variable to return a generic instance of the class, if it doesn't involve
                # variance (i.e. values of type variables are propagated). Our normal rules
                # would disallow this. Replace such return types with 'Any' to allow this.
                #
                # This could probably be more lenient (e.g. allow self type be nested, don't
                # require all type arguments to be identical to self_type), but this will
                # hopefully cover the vast majority of such cases, including Self.
                typ = erase_return_self_types(typ, self_type)

                typ2 = expand_type(typ, {tvar.id: object_type})
                if not is_subtype(typ, typ2):
                    co = False
                if not is_subtype(typ2, typ):
                    contra = False
                    if settable:
                        co = False

        # Infer variance from base classes, in case they have explicit variances
        for base in info.bases:
            base2 = expand_type(base, {tvar.id: object_type})
            if not is_subtype(base, base2):
                co = False
            if not is_subtype(base2, base):
                contra = False

        if co:
            v = COVARIANT
        elif contra:
            v = CONTRAVARIANT
        else:
            v = INVARIANT
        if v == variance:
            break
        tv.variance = VARIANCE_NOT_READY
    return True

