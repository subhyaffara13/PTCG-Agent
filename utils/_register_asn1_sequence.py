
def _register_asn1_sequence(cls: type[U]) -> None:
    raw_fields = typing.get_type_hints(cls, include_extras=True)
    root = declarative_asn1.Type.Sequence(cls, _annotate_fields(raw_fields))

    setattr(cls, "__asn1_root__", root)

