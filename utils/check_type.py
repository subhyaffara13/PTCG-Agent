
def check_type(context: str, obj: object, need: type = str) -> None:
    if type(obj) is not need:
        warn(
            f"{context!r} requires {need.__name__!r}, got {type(obj).__name__!r}.",
            WSGIWarning,
            stacklevel=3,
        )


def check_type(
    ctx_factory: Callable[[], tuple[JaxprPpContext, JaxprPpSettings]],
    env: dict[Var, Atom | MutableTypecheckVal],
    ty: AbstractValue,
  ) -> None:
  return  # Except in above case(s), all syntactic forms are valid

