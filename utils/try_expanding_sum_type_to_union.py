
def try_expanding_sum_type_to_union(typ: Type, target_fullname: str | None) -> Type:
    """Attempts to recursively expand any enum Instances with the given target_fullname
    into a Union of all of its component LiteralTypes.

    For example, if we have:

        class Color(Enum):
            RED = 1
            BLUE = 2
            YELLOW = 3

        class Status(Enum):
            SUCCESS = 1
            FAILURE = 2
            UNKNOWN = 3

    ...and if we call `try_expanding_sum_type_to_union(Union[Color, Status], 'module.Color')`,
    this function will return Literal[Color.RED, Color.BLUE, Color.YELLOW, Status].
    """
    typ = get_proper_type(typ)

    if isinstance(typ, UnionType):
        # Non-empty enums cannot subclass each other so simply removing duplicates is enough.
        items = [
            try_expanding_sum_type_to_union(item, target_fullname)
            for item in remove_dups(flatten_nested_unions(typ.relevant_items()))
        ]
        return UnionType.make_union(items)

    if isinstance(typ, Instance) and (
        target_fullname is None or typ.type.fullname == target_fullname
    ):
        if typ.type.fullname == "builtins.bool":
            return UnionType([LiteralType(True, typ), LiteralType(False, typ)])

        if typ.type.is_enum:
            items = [LiteralType(name, typ) for name in typ.type.enum_members]
            if not items:
                return typ
            return UnionType.make_union(items)

    return typ

