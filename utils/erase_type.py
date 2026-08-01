
def erase_type(typ: Type) -> ProperType:
    """Erase any type variables from a type.

    Also replace tuple types with the corresponding concrete types.

    Examples:
      A -> A
      B[X] -> B[Any]
      Tuple[A, B] -> tuple
      Callable[[A1, A2, ...], R] -> Callable[..., Any]
      Type[X] -> Type[Any]
    """
    typ = get_proper_type(typ)
    return typ.accept(EraseTypeVisitor())

