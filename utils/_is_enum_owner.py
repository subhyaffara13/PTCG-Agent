
def _is_enum_owner(owner: astroid.Instance | nodes.ClassDef) -> bool:
    """Return whether ``owner`` is an enum class or one of its members.

    Enums expose a dynamic ``__getattr__`` through their metaclass, but it is
    not invoked for attribute access on members, so -- unlike other owners with
    a dynamic ``__getattr__`` -- they must still be checked for ``no-member``
    (see https://github.com/pylint-dev/pylint/issues/2565).

    Callers are expected to have already narrowed ``owner`` to
    ``Instance | ClassDef``.
    """
    try:
        metaclass = owner.metaclass()
    except astroid.MroError:
        return False
    # ``EnumMeta`` was renamed to ``EnumType`` in Python 3.10.
    return metaclass is not None and metaclass.qname() in {
        "enum.EnumMeta",
        "enum.EnumType",
    }

