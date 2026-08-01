
def _transform_attrs(
    cls,
    these,
    auto_attribs,
    kw_only,
    collect_by_mro,
    field_transformer,
) -> _Attributes:
    """
    Transform all `_CountingAttr`s on a class into `Attribute`s.

    If *these* is passed, use that and don't look for them on the class.

    If *collect_by_mro* is True, collect them in the correct MRO order,
    otherwise use the old -- incorrect -- order.  See #428.

    Return an `_Attributes`.
    """
    cd = cls.__dict__
    anns = _get_annotations(cls)

    if these is not None:
        ca_list = list(these.items())
    elif auto_attribs is True:
        ca_names = {
            name
            for name, attr in cd.items()
            if attr.__class__ is _CountingAttr
        }
        ca_list = []
        annot_names = set()
        for attr_name, type in anns.items():
            if _is_class_var(type):
                continue
            annot_names.add(attr_name)
            a = cd.get(attr_name, NOTHING)

            if a.__class__ is not _CountingAttr:
                a = attrib(a)
            ca_list.append((attr_name, a))

        unannotated = ca_names - annot_names
        if unannotated:
            raise UnannotatedAttributeError(
                "The following `attr.ib`s lack a type annotation: "
                + ", ".join(
                    sorted(unannotated, key=lambda n: cd.get(n).counter)
                )
                + "."
            )
    else:
        ca_list = sorted(
            (
                (name, attr)
                for name, attr in cd.items()
                if attr.__class__ is _CountingAttr
            ),
            key=lambda e: e[1].counter,
        )

    fca = Attribute.from_counting_attr
    no = ClassProps.KeywordOnly.NO
    own_attrs = [
        fca(
            attr_name,
            ca,
            kw_only is not no,
            anns.get(attr_name),
        )
        for attr_name, ca in ca_list
    ]

    if collect_by_mro:
        base_attrs, base_attr_map = _collect_base_attrs(
            cls, {a.name for a in own_attrs}
        )
    else:
        base_attrs, base_attr_map = _collect_base_attrs_broken(
            cls, {a.name for a in own_attrs}
        )

    if kw_only is ClassProps.KeywordOnly.FORCE:
        own_attrs = [a.evolve(kw_only=True) for a in own_attrs]
        base_attrs = [a.evolve(kw_only=True) for a in base_attrs]

    attrs = base_attrs + own_attrs

    # Resolve default field alias before executing field_transformer, so that
    # the transformer receives fully populated Attribute objects with usable
    # alias values.
    for a in attrs:
        if not a.alias:
            # Evolve is very slow, so we hold our nose and do it dirty.
            _OBJ_SETATTR.__get__(a)("alias", _default_init_alias_for(a.name))
            _OBJ_SETATTR.__get__(a)("alias_is_default", True)

    if field_transformer is not None:
        attrs = tuple(field_transformer(cls, attrs))

    # Check attr order after executing the field_transformer.
    # Mandatory vs non-mandatory attr order only matters when they are part of
    # the __init__ signature and when they aren't kw_only (which are moved to
    # the end and can be mandatory or non-mandatory in any order, as they will
    # be specified as keyword args anyway). Check the order of those attrs:
    had_default = False
    for a in (a for a in attrs if a.init is not False and a.kw_only is False):
        if had_default is True and a.default is NOTHING:
            msg = f"No mandatory attributes allowed after an attribute with a default value or factory.  Attribute in question: {a!r}"
            raise ValueError(msg)

        if had_default is False and a.default is not NOTHING:
            had_default = True

    # Resolve default field alias for any new attributes that the
    # field_transformer may have added without setting an alias.
    for a in attrs:
        if not a.alias:
            _OBJ_SETATTR.__get__(a)("alias", _default_init_alias_for(a.name))
            _OBJ_SETATTR.__get__(a)("alias_is_default", True)

    # Create AttrsClass *after* applying the field_transformer since it may
    # add or remove attributes!
    attr_names = [a.name for a in attrs]
    AttrsClass = _make_attr_tuple_class(cls.__name__, attr_names)

    return _Attributes(AttrsClass(attrs), base_attrs, base_attr_map)

