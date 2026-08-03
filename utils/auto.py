from typing import Callable, Dict, List, Optional, Union

def auto(
    inputs: List[ArrayIndexType],
    output: ArrayIndexType,
    size_dict: Dict[str, int],
    memory_limit: Optional[int] = None,
) -> PathType:
    """Finds the contraction path by automatically choosing the method based on
    how many input arguments there are.
    """
    return _AUTO_CHOICES.get(len(inputs), greedy)(inputs, output, size_dict, memory_limit)


def auto(cls: Optional[Type[T]]) -> Type[T]:
    ...


def auto(*, angular: bool = False) -> Callable[[Type[T]], Type[T]]:
    ...


def auto(
    cls: Optional[Type[T]] = None, *, angular: Optional[bool] = None
) -> Union[Type[T], Callable[[Type[T]], Type[T]]]:
    """Class decorator to create __repr__ from __rich_repr__"""

    def do_replace(cls: Type[T], angular: Optional[bool] = None) -> Type[T]:
        def auto_repr(self: T) -> str:
            """Create repr string from __rich_repr__"""
            repr_str: List[str] = []
            append = repr_str.append

            angular: bool = getattr(self.__rich_repr__, "angular", False)  # type: ignore[attr-defined]
            for arg in self.__rich_repr__():  # type: ignore[attr-defined]
                if isinstance(arg, tuple):
                    if len(arg) == 1:
                        append(repr(arg[0]))
                    else:
                        key, value, *default = arg
                        if key is None:
                            append(repr(value))
                        else:
                            if default and default[0] == value:
                                continue
                            append(f"{key}={value!r}")
                else:
                    append(repr(arg))
            if angular:
                return f"<{self.__class__.__name__} {' '.join(repr_str)}>"
            else:
                return f"{self.__class__.__name__}({', '.join(repr_str)})"

        def auto_rich_repr(self: Type[T]) -> Result:
            """Auto generate __rich_rep__ from signature of __init__"""
            try:
                import inspect

                signature = inspect.signature(self.__init__)
                for name, param in signature.parameters.items():
                    if param.kind == param.POSITIONAL_ONLY:
                        yield getattr(self, name)
                    elif param.kind in (
                        param.POSITIONAL_OR_KEYWORD,
                        param.KEYWORD_ONLY,
                    ):
                        if param.default is param.empty:
                            yield getattr(self, param.name)
                        else:
                            yield param.name, getattr(self, param.name), param.default
            except Exception as error:
                raise ReprError(
                    f"Failed to auto generate __rich_repr__; {error}"
                ) from None

        if not hasattr(cls, "__rich_repr__"):
            auto_rich_repr.__doc__ = "Build a rich repr"
            cls.__rich_repr__ = auto_rich_repr  # type: ignore[attr-defined]

        auto_repr.__doc__ = "Return repr(self)"
        cls.__repr__ = auto_repr  # type: ignore[assignment]
        if angular is not None:
            cls.__rich_repr__.angular = angular  # type: ignore[attr-defined]
        return cls

    if cls is None:
        return partial(do_replace, angular=angular)
    else:
        return do_replace(cls, angular=angular)


def auto(cls: Optional[Type[T]]) -> Type[T]:
    ...


def auto(*, angular: bool = False) -> Callable[[Type[T]], Type[T]]:
    ...


def auto(
    cls: Optional[Type[T]] = None, *, angular: Optional[bool] = None
) -> Union[Type[T], Callable[[Type[T]], Type[T]]]:
    """Class decorator to create __repr__ from __rich_repr__"""

    def do_replace(cls: Type[T], angular: Optional[bool] = None) -> Type[T]:
        def auto_repr(self: T) -> str:
            """Create repr string from __rich_repr__"""
            repr_str: List[str] = []
            append = repr_str.append

            angular: bool = getattr(self.__rich_repr__, "angular", False)  # type: ignore[attr-defined]
            for arg in self.__rich_repr__():  # type: ignore[attr-defined]
                if isinstance(arg, tuple):
                    if len(arg) == 1:
                        append(repr(arg[0]))
                    else:
                        key, value, *default = arg
                        if key is None:
                            append(repr(value))
                        else:
                            if default and default[0] == value:
                                continue
                            append(f"{key}={value!r}")
                else:
                    append(repr(arg))
            if angular:
                return f"<{self.__class__.__name__} {' '.join(repr_str)}>"
            else:
                return f"{self.__class__.__name__}({', '.join(repr_str)})"

        def auto_rich_repr(self: Type[T]) -> Result:
            """Auto generate __rich_rep__ from signature of __init__"""
            try:
                signature = inspect.signature(self.__init__)
                for name, param in signature.parameters.items():
                    if param.kind == param.POSITIONAL_ONLY:
                        yield getattr(self, name)
                    elif param.kind in (
                        param.POSITIONAL_OR_KEYWORD,
                        param.KEYWORD_ONLY,
                    ):
                        if param.default is param.empty:
                            yield getattr(self, param.name)
                        else:
                            yield param.name, getattr(self, param.name), param.default
            except Exception as error:
                raise ReprError(
                    f"Failed to auto generate __rich_repr__; {error}"
                ) from None

        if not hasattr(cls, "__rich_repr__"):
            auto_rich_repr.__doc__ = "Build a rich repr"
            cls.__rich_repr__ = auto_rich_repr  # type: ignore[attr-defined]

        auto_repr.__doc__ = "Return repr(self)"
        cls.__repr__ = auto_repr  # type: ignore[assignment]
        if angular is not None:
            cls.__rich_repr__.angular = angular  # type: ignore[attr-defined]
        return cls

    if cls is None:
        return partial(do_replace, angular=angular)
    else:
        return do_replace(cls, angular=angular)

