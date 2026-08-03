import time

def data(func, dataname, *a, **kw):
    kw.setdefault('dataname', dataname)
    return FuncData(func, DATASETS_BOOST[dataname], *a, **kw)


def data():
    """
    Length-10 array for this type.

    * data[0] and data[1] should both be non missing
    * data[0] and data[1] should not be equal
    """
    raise NotImplementedError


def data(dtype):
    pa_dtype = dtype.pyarrow_dtype
    if pa.types.is_boolean(pa_dtype):
        data = [True, False] * 2 + [None] + [True, False] + [None] + [True, False]
    elif pa.types.is_floating(pa_dtype):
        data = [1.0, 0.0] * 2 + [None] + [-2.0, -1.0] + [None] + [0.5, 99.5]
    elif pa.types.is_signed_integer(pa_dtype):
        data = [1, 0] * 2 + [None] + [-2, -1] + [None] + [1, 99]
    elif pa.types.is_unsigned_integer(pa_dtype):
        data = [1, 0] * 2 + [None] + [2, 1] + [None] + [1, 99]
    elif pa.types.is_decimal(pa_dtype):
        data = (
            [Decimal("1"), Decimal("0.0")] * 2
            + [None]
            + [Decimal("-2.0"), Decimal("-1.0")]
            + [None]
            + [Decimal("0.5"), Decimal("33.123")]
        )
    elif pa.types.is_date(pa_dtype):
        data = (
            [date(2022, 1, 1), date(1999, 12, 31)] * 2
            + [None]
            + [date(2022, 1, 1), date(2022, 1, 1)]
            + [None]
            + [date(1999, 12, 31), date(1999, 12, 31)]
        )
    elif pa.types.is_timestamp(pa_dtype):
        data = (
            [datetime(2020, 1, 1, 1, 1, 1, 1), datetime(1999, 1, 1, 1, 1, 1, 1)] * 2
            + [None]
            + [datetime(2020, 1, 1, 1), datetime(1999, 1, 1, 1)]
            + [None]
            + [datetime(2020, 1, 1), datetime(1999, 1, 1)]
        )
    elif pa.types.is_duration(pa_dtype):
        data = (
            [timedelta(1), timedelta(1, 1)] * 2
            + [None]
            + [timedelta(-1), timedelta(0)]
            + [None]
            + [timedelta(-10), timedelta(10)]
        )
    elif pa.types.is_time(pa_dtype):
        data = (
            [time(12, 0), time(0, 12)] * 2
            + [None]
            + [time(0, 0), time(1, 1)]
            + [None]
            + [time(0, 5), time(5, 0)]
        )
    elif pa.types.is_string(pa_dtype):
        data = ["a", "b"] * 2 + [None] + ["1", "2"] + [None] + ["!", ">"]
    elif pa.types.is_binary(pa_dtype):
        data = [b"a", b"b"] * 2 + [None] + [b"1", b"2"] + [None] + [b"!", b">"]
    else:
        raise NotImplementedError
    return pd.array(data, dtype=dtype)


def data():
    """Length-100 array for this type.

    * data[0] and data[1] should both be non missing
    * data[0] and data[1] should not be equal
    """
    return Categorical(make_data(10))


def data(dtype):
    data = DatetimeArray._from_sequence(
        pd.date_range("2000", periods=10, tz=dtype.tz), dtype=dtype
    )
    return data


def data():
    arr = np.arange(10)
    return MyEA(arr)


def data():
    """Length-10 IntervalArray for semantics test."""
    return IntervalArray(make_data(10))


def data(dtype):
    if dtype.kind == "f":
        data = make_float_data()
    elif dtype.kind == "b":
        data = make_bool_data()
    else:
        data = make_data()
    return pd.array(data, dtype=dtype)


def data(allow_in_pandas, dtype):
    if dtype.numpy_dtype == "object":
        arr = pd.Series([(i,) for i in range(10)])._values
    else:
        arr = np.arange(1, 11, dtype=dtype._dtype)
    return NumpyExtensionArray(arr)


def data(dtype):
    return PeriodArray(np.arange(1970, 1980), dtype=dtype)


def data(request):
    """Length-10 SparseArray for semantics test."""
    res = SparseArray(make_data(request.param, 10), fill_value=request.param)
    return res


def data(dtype, chunked):
    strings = np.random.default_rng(2).choice(list(string.ascii_letters), size=10)
    while strings[0] == strings[1]:
        strings = np.random.default_rng(2).choice(list(string.ascii_letters), size=10)

    arr = dtype.construct_array_type()._from_sequence(strings, dtype=dtype)
    return maybe_split_array(arr, chunked)


def data():
    return DecimalArray(make_data(10))


def data():
    """Length-10 JSONArray for semantics test."""
    data = make_data(10)

    # Why the while loop? NumPy is unable to construct an ndarray from
    # equal-length ndarrays. Many of our operations involve coercing the
    # EA to an ndarray of objects. To avoid random test failures, we ensure
    # that our data is coercible to an ndarray. Several tests deal with only
    # the first two elements, so that's what we'll check.

    while len(data[0]) == len(data[1]):
        data = make_data(10)

    return JSONArray(data)


def data():
    """Length-10 ListArray for semantics test."""
    data = make_data(10)

    while len(data[0]) == len(data[1]):
        data = make_data(10)

    return ListArray(data)


def data():
    """Fixture returning boolean array with valid and missing values."""
    return pd.array(
        [True, False] * 2 + [np.nan] + [True, False] + [np.nan] + [True, False],
        dtype="boolean",
    )


def data():
    """Fixture returning boolean array with valid and missing data"""
    return pd.array(
        [True, False] * 2 + [np.nan] + [True, False] + [np.nan] + [True, False],
        dtype="boolean",
    )


def data():
    """Fixture returning boolean array, with valid and missing values."""
    return pd.array(
        [True, False] * 2 + [np.nan] + [True, False] + [np.nan] + [True, False],
        dtype="boolean",
    )


def data(dtype):
    """Fixture returning 'data' array according to parametrized float 'dtype'"""
    return pd.array(
        [0.1, 0.2, 0.3, 0.4, pd.NA, 1.0, 1.1, pd.NA, 9.9, 10.0],
        dtype=dtype,
    )


def data(dtype):
    """
    Fixture returning 'data' array with valid and missing values according to
    parametrized integer 'dtype'.

    Used to test dtype conversion with and without missing values.
    """
    return pd.array(
        [0, 1, 2, 3, pd.NA, 10, 11, pd.NA, 99, 100],
        dtype=dtype,
    )


def data(request):
    """Fixture returning parametrized (array, scalar) tuple.

    Used to test equivalence of scalars, numpy arrays with array ops, and the
    equivalence of DataFrame and Series ops.
    """
    return request.param


def data(request):
    """
    Fixture returning parametrized array from given dtype, including integer,
    float and boolean
    """
    return request.param


def data(request):
    """
    Fixture returning parametrized 'data' array with different integer and
    floating point types
    """
    return request.param


def data(value: A, /) -> A: ...


def data(
  *,
  default: A = dataclasses.MISSING,  # type: ignore[assignment]
  default_factory: tp.Callable[[], A] | None = None,  # type: ignore[assignment]
  init: bool = True,
  repr: bool = True,
  hash: bool | None = None,
  compare: bool = True,
  metadata: tp.Mapping[str, tp.Any] | None = None,
  kw_only: bool = False,
) -> tp.Any: ...


def data(value: tp.Any = MISSING, /, **kwargs) -> tp.Any:
  """Annotates a an attribute as pytree data.

  The return value from `data` must be directly assigned to an Object attribute
  which will be registered as a pytree data attribute.

  Example::

    from flax import nnx
    import jax

    class Foo(nnx.Pytree):
      def __init__(self):
        self.data_attr = nnx.data(42)  # pytree data
        self.static_attr = "hello"     # static attribute

    foo = Foo()

    assert jax.tree.leaves(foo) == [42]

  Args:
    value: The value to annotate as data.

  Returns:
    A value which will register the attribute as data on assignment.

  """
  if not isinstance(value, Missing) and kwargs:
    raise TypeError(
      'nnx.data() accepts either a single positional argument or keyword'
      ' arguments, but not both.'
    )
  metadata = {'nnx_value': value}
  if 'metadata' in kwargs and kwargs['metadata'] is not None:
    if 'static' in kwargs['metadata']:
      raise ValueError(
        "Cannot use 'static' key in metadata argument for nnx.data."
      )
    metadata.update(kwargs.pop('metadata'))
  metadata['static'] = False
  return dataclasses.field(**kwargs, metadata=metadata)  # type: ignore[return-value]

