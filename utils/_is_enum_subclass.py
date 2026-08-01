
def _is_enum_subclass(cls: nodes.ClassDef) -> bool:
    """Return whether cls is a subclass of an Enum."""
    return cls.is_subtype_of("enum.Enum")

