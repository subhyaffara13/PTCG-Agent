
def map_only(type_or_types_or_pred: type[T], /) -> MapOnlyFn[Fn[T, Any]]: ...


def map_only(type_or_types_or_pred: Type2[T, S], /) -> MapOnlyFn[Fn2[T, S, Any]]: ...


def map_only(
    type_or_types_or_pred: Type3[T, S, U], /
) -> MapOnlyFn[Fn3[T, S, U, Any]]: ...


def map_only(type_or_types_or_pred: TypeAny, /) -> MapOnlyFn[FnAny[Any]]: ...


def map_only(
    type_or_types_or_pred: Callable[[Any], bool], /
) -> MapOnlyFn[FnAny[Any]]: ...


def map_only(
    type_or_types_or_pred: TypeAny | Callable[[Any], bool], /
) -> MapOnlyFn[FnAny[Any]]:
    """
    Suppose you are writing a tree_map over tensors, leaving everything
    else unchanged.  Ordinarily you would have to write:

        def go(t):
            if isinstance(t, Tensor):
                return ...
            else:
                return t

    With this function, you only need to write:

        @map_only(Tensor)
        def go(t):
            return ...

    You can also directly use 'tree_map_only'
    """
    if isinstance(type_or_types_or_pred, (type, tuple, types.UnionType)):

        def pred(x: Any) -> bool:
            return isinstance(x, type_or_types_or_pred)  # type: ignore[arg-type]

    elif callable(type_or_types_or_pred):
        pred = type_or_types_or_pred  # type: ignore[assignment]
    else:
        raise TypeError("Argument must be a type, a tuple of types, or a callable.")

    def wrapper(func: Callable[[T], Any]) -> Callable[[Any], Any]:
        @functools.wraps(func)
        def wrapped(x: T) -> Any:
            if pred(x):
                return func(x)
            return x

        return wrapped

    return wrapper


def map_only(type_or_types_or_pred: type[T], /) -> MapOnlyFn[Fn[T, Any]]: ...


def map_only(type_or_types_or_pred: Type2[T, S], /) -> MapOnlyFn[Fn2[T, S, Any]]: ...


def map_only(
    type_or_types_or_pred: Type3[T, S, U], /
) -> MapOnlyFn[Fn3[T, S, U, Any]]: ...


def map_only(type_or_types_or_pred: TypeAny, /) -> MapOnlyFn[FnAny[Any]]: ...


def map_only(
    type_or_types_or_pred: Callable[[Any], bool], /
) -> MapOnlyFn[FnAny[Any]]: ...


def map_only(
    type_or_types_or_pred: TypeAny | Callable[[Any], bool], /
) -> MapOnlyFn[FnAny[Any]]:
    """
    Suppose you are writing a tree_map over tensors, leaving everything
    else unchanged.  Ordinarily you would have to write:

        def go(t):
            if isinstance(t, Tensor):
                return ...
            else:
                return t

    With this function, you only need to write:

        @map_only(Tensor)
        def go(t):
            return ...

    You can also directly use 'tree_map_only'
    """
    if isinstance(type_or_types_or_pred, (type, tuple, types.UnionType)):

        def pred(x: Any) -> bool:
            return isinstance(x, type_or_types_or_pred)  # type: ignore[arg-type]

    elif callable(type_or_types_or_pred):
        pred = type_or_types_or_pred  # type: ignore[assignment]
    else:
        raise TypeError("Argument must be a type, a tuple of types, or a callable.")

    def wrapper(func: Callable[[T], Any]) -> Callable[[Any], Any]:
        @functools.wraps(func)
        def wrapped(x: T) -> Any:
            if pred(x):
                return func(x)
            return x

        return wrapped

    return wrapper

