from typing import Callable, Optional, Union

def rich_repr(cls: Optional[Type[T]]) -> Type[T]:
    ...


def rich_repr(*, angular: bool = False) -> Callable[[Type[T]], Type[T]]:
    ...


def rich_repr(
    cls: Optional[Type[T]] = None, *, angular: bool = False
) -> Union[Type[T], Callable[[Type[T]], Type[T]]]:
    if cls is None:
        return auto(angular=angular)
    else:
        return auto(cls)


def rich_repr(cls: Optional[Type[T]]) -> Type[T]:
    ...


def rich_repr(*, angular: bool = False) -> Callable[[Type[T]], Type[T]]:
    ...


def rich_repr(
    cls: Optional[Type[T]] = None, *, angular: bool = False
) -> Union[Type[T], Callable[[Type[T]], Type[T]]]:
    if cls is None:
        return auto(angular=angular)
    else:
        return auto(cls)

