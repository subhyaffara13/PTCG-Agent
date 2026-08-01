
def attrs(
    maybe_cls=None,
    these=None,
    repr_ns=None,
    repr=None,
    cmp=None,
    hash=None,
    init=None,
    slots=False,
    frozen=False,
    weakref_slot=True,
    str=False,
    auto_attribs=False,
    kw_only=False,
    cache_hash=False,
    auto_exc=False,
    eq=None,
    order=None,
    auto_detect=False,
    collect_by_mro=False,
    getstate_setstate=None,
    on_setattr=None,
    field_transformer=None,
    match_args=True,
    unsafe_hash=None,
    force_kw_only=True,
):
    r"""
    A class decorator that adds :term:`dunder methods` according to the
    specified attributes using `attr.ib` or the *these* argument.

    Consider using `attrs.define` / `attrs.frozen` in new code (``attr.s`` will
    *never* go away, though).

    Args:
        repr_ns (str):
            When using nested classes, there was no way in Python 2 to
            automatically detect that.  This argument allows to set a custom
            name for a more meaningful ``repr`` output.  This argument is
            pointless in Python 3 and is therefore deprecated.

    .. caution::
        Refer to `attrs.define` for the rest of the parameters, but note that they
        can have different defaults.

        Notably, leaving *on_setattr* as `None` will **not** add any hooks.

    .. versionadded:: 16.0.0 *slots*
    .. versionadded:: 16.1.0 *frozen*
    .. versionadded:: 16.3.0 *str*
    .. versionadded:: 16.3.0 Support for ``__attrs_post_init__``.
    .. versionchanged:: 17.1.0
       *hash* supports `None` as value which is also the default now.
    .. versionadded:: 17.3.0 *auto_attribs*
    .. versionchanged:: 18.1.0
       If *these* is passed, no attributes are deleted from the class body.
    .. versionchanged:: 18.1.0 If *these* is ordered, the order is retained.
    .. versionadded:: 18.2.0 *weakref_slot*
    .. deprecated:: 18.2.0
       ``__lt__``, ``__le__``, ``__gt__``, and ``__ge__`` now raise a
       `DeprecationWarning` if the classes compared are subclasses of
       each other. ``__eq`` and ``__ne__`` never tried to compared subclasses
       to each other.
    .. versionchanged:: 19.2.0
       ``__lt__``, ``__le__``, ``__gt__``, and ``__ge__`` now do not consider
       subclasses comparable anymore.
    .. versionadded:: 18.2.0 *kw_only*
    .. versionadded:: 18.2.0 *cache_hash*
    .. versionadded:: 19.1.0 *auto_exc*
    .. deprecated:: 19.2.0 *cmp* Removal on or after 2021-06-01.
    .. versionadded:: 19.2.0 *eq* and *order*
    .. versionadded:: 20.1.0 *auto_detect*
    .. versionadded:: 20.1.0 *collect_by_mro*
    .. versionadded:: 20.1.0 *getstate_setstate*
    .. versionadded:: 20.1.0 *on_setattr*
    .. versionadded:: 20.3.0 *field_transformer*
    .. versionchanged:: 21.1.0
       ``init=False`` injects ``__attrs_init__``
    .. versionchanged:: 21.1.0 Support for ``__attrs_pre_init__``
    .. versionchanged:: 21.1.0 *cmp* undeprecated
    .. versionadded:: 21.3.0 *match_args*
    .. versionadded:: 22.2.0
       *unsafe_hash* as an alias for *hash* (for :pep:`681` compliance).
    .. deprecated:: 24.1.0 *repr_ns*
    .. versionchanged:: 24.1.0
       Instances are not compared as tuples of attributes anymore, but using a
       big ``and`` condition. This is faster and has more correct behavior for
       uncomparable values like `math.nan`.
    .. versionadded:: 24.1.0
       If a class has an *inherited* classmethod called
       ``__attrs_init_subclass__``, it is executed after the class is created.
    .. deprecated:: 24.1.0 *hash* is deprecated in favor of *unsafe_hash*.
    .. versionchanged:: 25.4.0
       *kw_only* now only applies to attributes defined in the current class,
       and respects attribute-level ``kw_only=False`` settings.
    .. versionadded:: 25.4.0 *force_kw_only*
    """
    if repr_ns is not None:
        import warnings

        warnings.warn(
            DeprecationWarning(
                "The `repr_ns` argument is deprecated and will be removed in or after August 2025."
            ),
            stacklevel=2,
        )

    eq_, order_ = _determine_attrs_eq_order(cmp, eq, order, None)

    #  unsafe_hash takes precedence due to PEP 681.
    if unsafe_hash is not None:
        hash = unsafe_hash

    if isinstance(on_setattr, (list, tuple)):
        on_setattr = setters.pipe(*on_setattr)

    def wrap(cls):
        nonlocal hash
        is_frozen = frozen or _has_frozen_base_class(cls)
        is_exc = auto_exc is True and issubclass(cls, BaseException)
        has_own_setattr = auto_detect and _has_own_attribute(
            cls, "__setattr__"
        )

        if has_own_setattr and is_frozen:
            msg = "Can't freeze a class with a custom __setattr__."
            raise ValueError(msg)

        eq = not is_exc and _determine_whether_to_implement(
            cls, eq_, auto_detect, ("__eq__", "__ne__")
        )

        Hashability = ClassProps.Hashability

        if is_exc:
            hashability = Hashability.LEAVE_ALONE
        elif hash is True:
            hashability = (
                Hashability.HASHABLE_CACHED
                if cache_hash
                else Hashability.HASHABLE
            )
        elif hash is False:
            hashability = Hashability.LEAVE_ALONE
        elif hash is None:
            if auto_detect is True and _has_own_attribute(cls, "__hash__"):
                hashability = Hashability.LEAVE_ALONE
            elif eq is True and is_frozen is True:
                hashability = (
                    Hashability.HASHABLE_CACHED
                    if cache_hash
                    else Hashability.HASHABLE
                )
            elif eq is False:
                hashability = Hashability.LEAVE_ALONE
            else:
                hashability = Hashability.UNHASHABLE
        else:
            msg = "Invalid value for hash.  Must be True, False, or None."
            raise TypeError(msg)

        KeywordOnly = ClassProps.KeywordOnly
        if kw_only:
            kwo = KeywordOnly.FORCE if force_kw_only else KeywordOnly.YES
        else:
            kwo = KeywordOnly.NO

        props = ClassProps(
            is_exception=is_exc,
            is_frozen=is_frozen,
            is_slotted=slots,
            collected_fields_by_mro=collect_by_mro,
            added_init=_determine_whether_to_implement(
                cls, init, auto_detect, ("__init__",)
            ),
            added_repr=_determine_whether_to_implement(
                cls, repr, auto_detect, ("__repr__",)
            ),
            added_eq=eq,
            added_ordering=not is_exc
            and _determine_whether_to_implement(
                cls,
                order_,
                auto_detect,
                ("__lt__", "__le__", "__gt__", "__ge__"),
            ),
            hashability=hashability,
            added_match_args=match_args,
            kw_only=kwo,
            has_weakref_slot=weakref_slot,
            added_str=str,
            added_pickling=_determine_whether_to_implement(
                cls,
                getstate_setstate,
                auto_detect,
                ("__getstate__", "__setstate__"),
                default=slots,
            ),
            on_setattr_hook=on_setattr,
            field_transformer=field_transformer,
        )

        if not props.is_hashable and cache_hash:
            msg = "Invalid value for cache_hash.  To use hash caching, hashing must be either explicitly or implicitly enabled."
            raise TypeError(msg)

        builder = _ClassBuilder(
            cls,
            these,
            auto_attribs=auto_attribs,
            props=props,
            has_custom_setattr=has_own_setattr,
        )

        if props.added_repr:
            builder.add_repr(repr_ns)

        if props.added_str:
            builder.add_str()

        if props.added_eq:
            builder.add_eq()
        if props.added_ordering:
            builder.add_order()

        if not frozen:
            builder.add_setattr()

        if props.is_hashable:
            builder.add_hash()
        elif props.hashability is Hashability.UNHASHABLE:
            builder.make_unhashable()

        if props.added_init:
            builder.add_init()
        else:
            builder.add_attrs_init()
            if cache_hash:
                msg = "Invalid value for cache_hash.  To use hash caching, init must be True."
                raise TypeError(msg)

        if PY_3_13_PLUS and not _has_own_attribute(cls, "__replace__"):
            builder.add_replace()

        if (
            PY_3_10_PLUS
            and match_args
            and not _has_own_attribute(cls, "__match_args__")
        ):
            builder.add_match_args()

        return builder.build_class()

    # maybe_cls's type depends on the usage of the decorator.  It's a class
    # if it's used as `@attrs` but `None` if used as `@attrs()`.
    if maybe_cls is None:
        return wrap

    return wrap(maybe_cls)

