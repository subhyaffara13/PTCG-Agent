
def serializable_enum(cls: Literal[None] = None) -> Callable[[Type[_E]], Type[_E]]:
    ...


def serializable_enum(cls: Type[_E]) -> Type[_E]:  # type:ignore[misc] # mypy on py37
    ...


def serializable_enum(cls: Optional[Type[_E]] = None) -> Union[
    Callable[[Type[_E]], Type[_E]],
    Type[_E]
]:
    """Decorator"""

    def decorate(kls: Type[_E]) -> Type[_E]:
        ObjectMetadataLibrary.register_enum(klass=kls)
        return kls

    # See if we're being called as @enum or @enum().
    if cls is None:
        # We're called with parens.
        return decorate

    # We're called as @register_klass without parens.
    return decorate(cls)

