
def value_set(
    value_type: type,
) -> typing.Callable[[type[U]], type[U]]:
    """
    A class decorator that registers an `enum.Enum` subclass as an
    ASN.1 value set of the given underlying type. All the member
    values must be instances of `value_type`. Members are encoded as
    their value; decoding fails if the decoded value does not match
    any member.
    """
    rust_type = declarative_asn1.non_root_python_to_rust(value_type)

    def decorator(cls: type[U]) -> type[U]:
        if not issubclass(cls, enum.Enum):
            raise TypeError(
                "value sets can only be defined from enum.Enum subclasses"
            )
        members = list(cls)
        if not members:
            raise TypeError(
                f"value set '{cls.__name__}' must have at least one member"
            )
        for member in members:
            if not isinstance(member.value, value_type):
                raise TypeError(
                    f"member '{member.name}' of value set '{cls.__name__}' "
                    f"must have a value of type "
                    f"'{value_type.__name__}', got: "
                    f"'{type(member.value).__name__}'"
                )
        inner = declarative_asn1.AnnotatedType(
            rust_type, declarative_asn1.Annotation()
        )
        # Map from member value to member, used for O(1) lookups when
        # decoding. This requires the member values to be hashable.
        value_map = {member.value: member for member in members}
        root = declarative_asn1.Type.ValueSet(cls, inner, value_map)

        setattr(cls, "__asn1_root__", root)
        return cls

    return decorator

