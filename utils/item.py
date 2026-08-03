import time
from typing import Any

def item(value: bool, _parent: Item | None = ..., _sort_keys: bool = ...) -> Bool: ...  # type: ignore[overload-overlap]


def item(value: int, _parent: Item | None = ..., _sort_keys: bool = ...) -> Integer: ...


def item(value: float, _parent: Item | None = ..., _sort_keys: bool = ...) -> Float: ...


def item(value: str, _parent: Item | None = ..., _sort_keys: bool = ...) -> String: ...


def item(  # type: ignore[overload-overlap]
    value: datetime, _parent: Item | None = ..., _sort_keys: bool = ...
) -> DateTime: ...


def item(value: date, _parent: Item | None = ..., _sort_keys: bool = ...) -> Date: ...


def item(value: time, _parent: Item | None = ..., _sort_keys: bool = ...) -> Time: ...


def item(
    value: Sequence[dict[str, Any]], _parent: Item | None = ..., _sort_keys: bool = ...
) -> AoT: ...


def item(
    value: Sequence[Any], _parent: Item | None = ..., _sort_keys: bool = ...
) -> Array: ...


def item(
    value: dict[str, Any], _parent: Array = ..., _sort_keys: bool = ...
) -> InlineTable: ...


def item(
    value: dict[str, Any], _parent: Item | None = ..., _sort_keys: bool = ...
) -> Table: ...


def item(value: ItemT, _parent: Item | None = ..., _sort_keys: bool = ...) -> ItemT: ...


def item(value: object, _parent: Item | None = ..., _sort_keys: bool = ...) -> Item: ...


def item(value: Any, _parent: Item | None = None, _sort_keys: bool = False) -> Item:
    """Create a TOML item from a Python object.

    :Example:

    >>> item(42)
    42
    >>> item([1, 2, 3])
    [1, 2, 3]
    >>> item({'a': 1, 'b': 2})
    a = 1
    b = 2
    """

    from tomlkit.container import Container

    if isinstance(value, Item):
        return value

    if isinstance(value, bool):
        return Bool(value, Trivia())
    elif isinstance(value, int):
        return Integer(value, Trivia(), str(value))
    elif isinstance(value, float):
        return Float(value, Trivia(), str(value))
    elif isinstance(value, dict):
        table_constructor = (
            InlineTable if isinstance(_parent, (Array, InlineTable)) else Table
        )
        val = table_constructor(Container(), Trivia(), False)
        for k, v in sorted(
            value.items(),
            key=lambda i: (isinstance(i[1], dict), i[0]) if _sort_keys else 1,
        ):
            val[k] = item(v, _parent=val, _sort_keys=_sort_keys)

        return val
    elif isinstance(value, (list, tuple)):
        a: AoT | Array
        if (
            value
            and all(isinstance(v, dict) for v in value)
            and (_parent is None or isinstance(_parent, Table))
        ):
            a = AoT([])
            table_constructor = Table
        else:
            a = Array([], Trivia())
            table_constructor = InlineTable

        for v in value:
            if isinstance(v, dict):
                table = table_constructor(Container(), Trivia(), True)

                for k, _v in sorted(
                    v.items(),
                    key=lambda i: (isinstance(i[1], dict), i[0] if _sort_keys else 1),
                ):
                    i = item(_v, _parent=table, _sort_keys=_sort_keys)
                    if isinstance(table, InlineTable):
                        i.trivia.trail = ""

                    table[k] = i

                v = table

            a.append(v)

        return a
    elif isinstance(value, str):
        return String.from_raw(value)
    elif isinstance(value, datetime):
        return DateTime(
            value.year,
            value.month,
            value.day,
            value.hour,
            value.minute,
            value.second,
            value.microsecond,
            value.tzinfo,
            Trivia(),
            value.isoformat().replace("+00:00", "Z"),
        )
    elif isinstance(value, date):
        return Date(value.year, value.month, value.day, Trivia(), value.isoformat())
    elif isinstance(value, time):
        return Time(
            value.hour,
            value.minute,
            value.second,
            value.microsecond,
            value.tzinfo,
            Trivia(),
            value.isoformat(),
        )
    else:
        for encoder in CUSTOM_ENCODERS:
            try:
                # Check if encoder accepts keyword arguments for backward compatibility
                sig = inspect.signature(encoder)
                if "_parent" in sig.parameters or any(
                    p.kind == p.VAR_KEYWORD for p in sig.parameters.values()
                ):
                    # New style encoder that can accept additional parameters
                    rv = encoder(value, _parent=_parent, _sort_keys=_sort_keys)  # type: ignore[call-arg]
                else:
                    # Old style encoder that only accepts value
                    rv = encoder(value)
            except ConvertError:
                pass
            else:
                if not isinstance(rv, Item):
                    raise ConvertError(
                        f"Custom encoder is expected to return an instance of Item, got {type(rv)}"
                    )
                return rv

    raise ConvertError(f"Unable to convert an object of {type(value)} to a TOML item")


def item(a: TensorLikeType) -> NumberType:
    if a.numel() != 1:
        msg = f"Can't convert a tensor with {a.numel()} elements to a number!"
        raise ValueError(msg)

    # NOTE: explicit conversion is necessary for bool!
    # See https://github.com/pytorch/pytorch/issues/78071
    number_type = utils.dtype_to_type(a.dtype)
    return number_type(prims.item(a))


def item(g: jit_utils.GraphContext, self):
    return self


def item(request):
    key, data = request.param
    return key, data

