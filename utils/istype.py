from typing import Any

def istype(obj: object, allowed_types: type[T]) -> TypeIs[T]: ...


def istype(
    obj: object, allowed_types: tuple[type[list[T]], type[tuple[T, ...]]]
) -> TypeIs[T]: ...


def istype(
    obj: object, allowed_types: tuple[type[T1], type[T2]]
) -> TypeIs[T1 | T2]: ...


def istype(
    obj: object, allowed_types: tuple[type[T1], type[T2], type[T3]]
) -> TypeIs[T1 | T2 | T3]: ...


def istype(
    obj: object, allowed_types: tuple[type[T1], type[T2], type[T3], type[T4]]
) -> TypeIs[T1 | T2 | T3 | T4]: ...


def istype(
    obj: object, allowed_types: tuple[type[T1], type[T2], type[T3], type[T4], type[T5]]
) -> TypeIs[T1 | T2 | T3 | T4 | T5]: ...


def istype(
    obj: object,
    allowed_types: tuple[type[T1], type[T2], type[T3], type[T4], type[T5], type[T6]],
) -> TypeIs[T1 | T2 | T3 | T4 | T5 | T6]: ...


def istype(
    obj: object,
    allowed_types: tuple[
        type[T1], type[T2], type[T3], type[T4], type[T5], type[T6], type[T7]
    ],
) -> TypeIs[T1 | T2 | T3 | T4 | T5 | T6 | T7]: ...


def istype(
    obj: object,
    allowed_types: tuple[
        type[T1], type[T2], type[T3], type[T4], type[T5], type[T6], type[T7], type[T8]
    ],
) -> TypeIs[T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8]: ...


def istype(
    obj: object,
    allowed_types: tuple[
        type[T1],
        type[T2],
        type[T3],
        type[T4],
        type[T5],
        type[T6],
        type[T7],
        type[T8],
        type[T9],
    ],
) -> TypeIs[T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 | T9]: ...


def istype(
    obj: object,
    allowed_types: tuple[
        type[T1],
        type[T2],
        type[T3],
        type[T4],
        type[T5],
        type[T6],
        type[T7],
        type[T8],
        type[T9],
        type[T10],
    ],
) -> TypeIs[T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 | T9 | T10]: ...


def istype(
    obj: object, allowed_types: tuple[type, ...] | list[type] | set[type]
) -> bool: ...


def istype(obj: object, allowed_types: Any) -> bool:
    """isinstance() without subclasses"""
    if isinstance(allowed_types, (tuple, list, set)):
        return type(obj) in allowed_types
    return type(obj) is allowed_types

