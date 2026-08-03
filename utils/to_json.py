from typing import Any, Callable

def to_json(
    path_or_buf: FilePath | WriteBuffer[str] | WriteBuffer[bytes],
    obj: NDFrame,
    orient: str | None = ...,
    date_format: str = ...,
    double_precision: int = ...,
    force_ascii: bool = ...,
    date_unit: str = ...,
    default_handler: Callable[[Any], JSONSerializable] | None = ...,
    lines: bool = ...,
    compression: CompressionOptions = ...,
    index: bool | None = ...,
    indent: int = ...,
    storage_options: StorageOptions = ...,
    mode: Literal["a", "w"] = ...,
) -> None: ...


def to_json(
    path_or_buf: None,
    obj: NDFrame,
    orient: str | None = ...,
    date_format: str = ...,
    double_precision: int = ...,
    force_ascii: bool = ...,
    date_unit: str = ...,
    default_handler: Callable[[Any], JSONSerializable] | None = ...,
    lines: bool = ...,
    compression: CompressionOptions = ...,
    index: bool | None = ...,
    indent: int = ...,
    storage_options: StorageOptions = ...,
    mode: Literal["a", "w"] = ...,
) -> str: ...


def to_json(
    path_or_buf: FilePath | WriteBuffer[str] | WriteBuffer[bytes] | None,
    obj: NDFrame,
    orient: str | None = None,
    date_format: str = "epoch",
    double_precision: int = 10,
    force_ascii: bool = True,
    date_unit: str = "ms",
    default_handler: Callable[[Any], JSONSerializable] | None = None,
    lines: bool = False,
    compression: CompressionOptions = "infer",
    index: bool | None = None,
    indent: int = 0,
    storage_options: StorageOptions | None = None,
    mode: Literal["a", "w"] = "w",
) -> str | None:
    if orient in ["records", "values"] and index is True:
        raise ValueError(
            "'index=True' is only valid when 'orient' is 'split', 'table', "
            "'index', or 'columns'."
        )
    elif orient in ["index", "columns"] and index is False:
        raise ValueError(
            "'index=False' is only valid when 'orient' is 'split', 'table', "
            "'records', or 'values'."
        )
    elif index is None:
        # will be ignored for orient='records' and 'values'
        index = True

    if lines and orient != "records":
        raise ValueError("'lines' keyword only valid when 'orient' is records")

    if mode not in ["a", "w"]:
        msg = (
            f"mode={mode} is not a valid option."
            "Only 'w' and 'a' are currently supported."
        )
        raise ValueError(msg)

    if mode == "a" and (not lines or orient != "records"):
        msg = (
            "mode='a' (append) is only supported when "
            "lines is True and orient is 'records'"
        )
        raise ValueError(msg)

    if orient == "table" and isinstance(obj, Series):
        obj = obj.to_frame(name=obj.name or "values")

    if date_format == "epoch":
        # for epoch (numeric) format, convert datetime-likes to the desired
        # unit up front, such that the C ObjToJSON code can simply write out
        # the integer values without worrying about conversion
        if date_unit not in ["s", "ms", "us", "ns"]:
            raise ValueError(f"Invalid value '{date_unit}' for option 'date_unit'")
        if isinstance(obj, DataFrame):
            copied = False
            cols = np.nonzero(obj.dtypes.map(lambda dt: dt.kind in ["M", "m"]))[0]
            if len(cols):
                obj = obj.copy(deep=False)
                copied = True
                for col in cols:
                    obj.isetitem(col, obj.iloc[:, col].dt.as_unit(date_unit))
            if obj.index.dtype.kind in "Mm":
                if not copied:
                    obj = obj.copy(deep=False)
                    copied = True
                obj.index = Series(obj.index).dt.as_unit(date_unit)
            if obj.columns.dtype.kind in "Mm":
                if not copied:
                    obj = obj.copy(deep=False)
                    copied = True
                obj.columns = Series(obj.columns).dt.as_unit(date_unit)
        elif isinstance(obj, Series):
            if obj.dtype.kind in "Mm":
                obj = obj.copy(deep=False)
                obj = obj.dt.as_unit(date_unit)
            if obj.index.dtype.kind in "Mm":
                obj = obj.copy(deep=False)
                obj.index = Series(obj.index).dt.as_unit(date_unit)

    writer: type[Writer]
    if orient == "table" and isinstance(obj, DataFrame):
        writer = JSONTableWriter
    elif isinstance(obj, Series):
        writer = SeriesWriter
    elif isinstance(obj, DataFrame):
        writer = FrameWriter
    else:
        raise NotImplementedError("'obj' should be a Series or a DataFrame")

    s = writer(
        obj,
        orient=orient,
        date_format=date_format,
        double_precision=double_precision,
        ensure_ascii=force_ascii,
        date_unit=date_unit,
        default_handler=default_handler,
        index=index,
        indent=indent,
    ).write()

    if lines:
        s = convert_to_line_delimits(s)

    if path_or_buf is not None:
        # apply compression and byte/text conversion
        with get_handle(
            path_or_buf, mode, compression=compression, storage_options=storage_options
        ) as handles:
            handles.handle.write(s)
    else:
        return s
    return None


def to_json(state):
    if isinstance(state, np.ndarray):
        return state.tolist()
    elif isinstance(state, np.int64):
        return state.tolist()
    elif isinstance(state, list):
        return [to_json(s) for s in state]
    elif isinstance(state, dict):
        out = {}
        for k in state:
            out[k] = to_json(state[k])
        return out
    else:
        return state


def to_json(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, list) or isinstance(obj, tuple):
        return [to_json(s) for s in obj]
    elif isinstance(obj, dict):
        out = {}
        for k in obj:
            out[k] = to_json(obj[k])
        return out
    else:
        return obj

