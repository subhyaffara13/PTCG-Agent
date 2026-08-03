import copy
from typing import Any

def array(sound):
    """pygame.sndarray.array(Sound): return array

    Copy Sound samples into an array.

    Creates a new array for the sound data and copies the samples. The
    array will always be in the format returned from
    pygame.mixer.get_init().
    """

    return numpy.array(sound, copy=True)


def array(raw: str = "[]") -> Array:
    """Create an array item for its string representation.

    :Example:

    >>> array("[1, 2, 3]")  # Create from a string
    [1, 2, 3]
    >>> a = array()
    >>> a.extend([1, 2, 3])  # Create from a list
    >>> a
    [1, 2, 3]
    """
    v = value(raw)
    if not isinstance(v, Array):
        raise ValueError(f"Expected an array, got {type(v)}")
    return v


def array(obj, dtype=None, *, copy=True, order="K", subok=False, ndmin=0, like=None):
    if subok is not False:
        raise NotImplementedError("'subok' parameter is not supported.")
    if like is not None:
        raise NotImplementedError("'like' parameter is not supported.")
    if order != "K":
        raise NotImplementedError

    # a happy path
    if (
        isinstance(obj, ndarray)
        and copy is False
        and dtype is None
        and ndmin <= obj.ndim
    ):
        return obj

    if isinstance(obj, (list, tuple)):
        # FIXME and they have the same dtype, device, etc
        if obj and all(isinstance(x, torch.Tensor) for x in obj):
            # list of arrays: *under torch.Dynamo* these are FakeTensors
            obj = torch.stack(obj)
        else:
            # XXX: remove tolist
            # lists of ndarrays: [1, [2, 3], ndarray(4)] convert to lists of lists
            obj = _tolist(obj)

    # is obj an ndarray already?
    if isinstance(obj, ndarray):
        obj = obj.tensor

    # is a specific dtype requested?
    torch_dtype = None
    if dtype is not None:
        torch_dtype = _dtypes.dtype(dtype).torch_dtype

    tensor = _util._coerce_to_tensor(obj, torch_dtype, copy, ndmin)
    return ndarray(tensor)


def array(symbol, dim, intent=None, *, attrs=(), value=None, type=None):
    """ Convenience function for creating a Variable instance for a Fortran array.

    Parameters
    ==========

    symbol : symbol
    dim : Attribute or iterable
        If dim is an ``Attribute`` it need to have the name 'dimension'. If it is
        not an ``Attribute``, then it is passed to :func:`dimension` as ``*dim``
    intent : str
        One of: 'in', 'out', 'inout' or None
    \\*\\*kwargs:
        Keyword arguments for ``Variable`` ('type' & 'value')

    Examples
    ========

    >>> from sympy import fcode
    >>> from sympy.codegen.ast import integer, real
    >>> from sympy.codegen.fnodes import array
    >>> arr = array('a', '*', 'in', type=integer)
    >>> print(fcode(arr.as_Declaration(), source_format='free', standard=2003))
    integer*4, dimension(*), intent(in) :: a
    >>> x = array('x', [3, ':', ':'], intent='out', type=real)
    >>> print(fcode(x.as_Declaration(value=1), source_format='free', standard=2003))
    real*8, dimension(3, :, :), intent(out) :: x = 1

    """
    if isinstance(dim, Attribute):
        if str(dim.name) != 'dimension':
            raise ValueError("Got an unexpected Attribute argument as dim: %s" % str(dim))
    else:
        dim = dimension(*dim)

    attrs = list(attrs) + [dim]
    if intent is not None:
        if intent not in (intent_in, intent_out, intent_inout):
            intent = {'in': intent_in, 'out': intent_out, 'inout': intent_inout}[intent]
        attrs.append(intent)
    if type is None:
        return Variable.deduced(symbol, value=value, attrs=attrs)
    else:
        return Variable(symbol, type, value=value, attrs=attrs)


def array(
    data: Sequence[object] | AnyArrayLike,
    dtype: Dtype | None = None,
    copy: bool = True,
) -> ExtensionArray:
    """
    Create an array.

    This method constructs an array using pandas extension types when possible.
    If `dtype` is specified, it determines the type of array returned. Otherwise,
    pandas attempts to infer the appropriate dtype based on `data`.

    Parameters
    ----------
    data : Sequence of objects
        The scalars inside `data` should be instances of the
        scalar type for `dtype`. It's expected that `data`
        represents a 1-dimensional array of data.

        When `data` is an Index or Series, the underlying array
        will be extracted from `data`.

    dtype : str, np.dtype, or ExtensionDtype, optional
        The dtype to use for the array. This may be a NumPy
        dtype or an extension type registered with pandas using
        :meth:`pandas.api.extensions.register_extension_dtype`.

        If not specified, there are two possibilities:

        1. When `data` is a :class:`Series`, :class:`Index`, or
           :class:`ExtensionArray`, the `dtype` will be taken
           from the data.
        2. Otherwise, pandas will attempt to infer the `dtype`
           from the data.

        Note that when `data` is a NumPy array, ``data.dtype`` is
        *not* used for inferring the array type. This is because
        NumPy cannot represent all the types of data that can be
        held in extension arrays.

        Currently, pandas will infer an extension dtype for sequences of

        ============================== =======================================
        Scalar Type                    Array Type
        ============================== =======================================
        :class:`pandas.Interval`       :class:`pandas.arrays.IntervalArray`
        :class:`pandas.Period`         :class:`pandas.arrays.PeriodArray`
        :class:`datetime.datetime`     :class:`pandas.arrays.DatetimeArray`
        :class:`datetime.timedelta`    :class:`pandas.arrays.TimedeltaArray`
        :class:`int`                   :class:`pandas.arrays.IntegerArray`
        :class:`float`                 :class:`pandas.arrays.FloatingArray`
        :class:`str`                   :class:`pandas.arrays.StringArray` or
                                       :class:`pandas.arrays.ArrowStringArray`
        :class:`bool`                  :class:`pandas.arrays.BooleanArray`
        ============================== =======================================

        The ExtensionArray created when the scalar type is :class:`str` is determined by
        ``pd.options.mode.string_storage`` if the dtype is not explicitly given.

        For all other cases, NumPy's usual inference rules will be used.
    copy : bool, default True
        Whether to copy the data, even if not necessary. Depending
        on the type of `data`, creating the new array may require
        copying data, even if ``copy=False``.

    Returns
    -------
    ExtensionArray
        The newly created array.

    Raises
    ------
    ValueError
        When `data` is not 1-dimensional.

    See Also
    --------
    numpy.array : Construct a NumPy array.
    Series : Construct a pandas Series.
    Index : Construct a pandas Index.
    arrays.NumpyExtensionArray : ExtensionArray wrapping a NumPy array.
    Series.array : Extract the array stored within a Series.

    Notes
    -----
    Omitting the `dtype` argument means pandas will attempt to infer the
    best array type from the values in the data. As new array types are
    added by pandas and 3rd party libraries, the "best" array type may
    change. We recommend specifying `dtype` to ensure that

    1. the correct array type for the data is returned
    2. the returned array type doesn't change as new extension types
       are added by pandas and third-party libraries

    Additionally, if the underlying memory representation of the returned
    array matters, we recommend specifying the `dtype` as a concrete object
    rather than a string alias or allowing it to be inferred. For example,
    a future version of pandas or a 3rd-party library may include a
    dedicated ExtensionArray for string data. In this event, the following
    would no longer return a :class:`arrays.NumpyExtensionArray` backed by a
    NumPy array.

    >>> pd.array(["a", "b"], dtype=str)
    <ArrowStringArray>
    ['a', 'b']
    Length: 2, dtype: str

    This would instead return the new ExtensionArray dedicated for string
    data. If you really need the new array to be backed by a  NumPy array,
    specify that in the dtype.

    >>> pd.array(["a", "b"], dtype=np.dtype("<U1"))
    <NumpyExtensionArray>
    ['a', 'b']
    Length: 2, dtype: str32

    Finally, Pandas has arrays that mostly overlap with NumPy

      * :class:`arrays.DatetimeArray`
      * :class:`arrays.TimedeltaArray`

    When data with a ``datetime64[ns]`` or ``timedelta64[ns]`` dtype is
    passed, pandas will always return a ``DatetimeArray`` or ``TimedeltaArray``
    rather than a ``NumpyExtensionArray``. This is for symmetry with the case of
    timezone-aware data, which NumPy does not natively support.

    >>> pd.array(["2015", "2016"], dtype="datetime64[ns]")
    <DatetimeArray>
    ['2015-01-01 00:00:00', '2016-01-01 00:00:00']
    Length: 2, dtype: datetime64[ns]

    >>> pd.array(["1h", "2h"], dtype="timedelta64[ns]")
    <TimedeltaArray>
    ['0 days 01:00:00', '0 days 02:00:00']
    Length: 2, dtype: timedelta64[ns]

    Examples
    --------
    If a dtype is not specified, pandas will infer the best dtype from the values.
    See the description of `dtype` for the types pandas infers for.

    >>> pd.array([1, 2])
    <IntegerArray>
    [1, 2]
    Length: 2, dtype: Int64

    >>> pd.array([1, 2, np.nan])
    <IntegerArray>
    [1, 2, <NA>]
    Length: 3, dtype: Int64

    >>> pd.array([1.1, 2.2])
    <FloatingArray>
    [1.1, 2.2]
    Length: 2, dtype: Float64

    >>> pd.array(["a", None, "c"])
    <ArrowStringArray>
    ['a', <NA>, 'c']
    Length: 3, dtype: string

    >>> with pd.option_context("string_storage", "python"):
    ...     arr = pd.array(["a", None, "c"])
    >>> arr
    <StringArray>
    ['a', <NA>, 'c']
    Length: 3, dtype: string

    >>> pd.array([pd.Period("2000", freq="D"), pd.Period("2000", freq="D")])
    <PeriodArray>
    ['2000-01-01', '2000-01-01']
    Length: 2, dtype: period[D]

    You can use the string alias for `dtype`

    >>> pd.array(["a", "b", "a"], dtype="category")
    ['a', 'b', 'a']
    Categories (2, str): ['a', 'b']

    Or specify the actual dtype

    >>> pd.array(
    ...     ["a", "b", "a"], dtype=pd.CategoricalDtype(["a", "b", "c"], ordered=True)
    ... )
    ['a', 'b', 'a']
    Categories (3, str): ['a' < 'b' < 'c']

    If pandas does not infer a dedicated extension type a
    :class:`arrays.NumpyExtensionArray` is returned.

    >>> pd.array([1 + 1j, 3 + 2j])
    <NumpyExtensionArray>
    [(1+1j), (3+2j)]
    Length: 2, dtype: complex128

    As mentioned in the "Notes" section, new extension types may be added
    in the future (by pandas or 3rd party libraries), causing the return
    value to no longer be a :class:`arrays.NumpyExtensionArray`. Specify the
    `dtype` as a NumPy dtype if you need to ensure there's no future change in
    behavior.

    >>> pd.array([1, 2], dtype=np.dtype("int32"))
    <NumpyExtensionArray>
    [1, 2]
    Length: 2, dtype: int32

    `data` must be 1-dimensional. A ValueError is raised when the input
    has the wrong dimensionality.

    >>> pd.array(1)
    Traceback (most recent call last):
      ...
    ValueError: Cannot pass scalar '1' to 'pandas.array'.
    """
    from pandas.core.arrays import (
        BooleanArray,
        DatetimeArray,
        ExtensionArray,
        FloatingArray,
        IntegerArray,
        NumpyExtensionArray,
        TimedeltaArray,
    )
    from pandas.core.arrays.string_ import StringDtype

    if lib.is_scalar(data):
        msg = f"Cannot pass scalar '{data}' to 'pandas.array'."
        raise ValueError(msg)
    elif isinstance(data, ABCDataFrame):
        raise TypeError("Cannot pass DataFrame to 'pandas.array'")

    if dtype is None and isinstance(data, (ABCSeries, ABCIndex, ExtensionArray)):
        # Note: we exclude np.ndarray here, will do type inference on it
        dtype = data.dtype

    data = extract_array(data, extract_numpy=True)

    # this returns None for not-found dtypes.
    if dtype is not None:
        dtype = pandas_dtype(dtype)

    if isinstance(data, ExtensionArray) and (dtype is None or data.dtype == dtype):
        # e.g. TimedeltaArray[s], avoid casting to NumpyExtensionArray
        if copy:
            return data.copy()
        return data

    if isinstance(dtype, ExtensionDtype):
        cls = dtype.construct_array_type()
        return cls._from_sequence(data, dtype=dtype, copy=copy)

    if dtype is None:
        was_ndarray = isinstance(data, np.ndarray)
        # error: Item "Sequence[object]" of "Sequence[object] | ExtensionArray |
        # ndarray[Any, Any]" has no attribute "dtype"
        if not was_ndarray or data.dtype == object:  # type: ignore[union-attr]
            result = lib.maybe_convert_objects(
                ensure_object(data),
                convert_non_numeric=True,
                convert_to_nullable_dtype=True,
                dtype_if_all_nat=np.dtype("M8[s]"),
            )
            result = ensure_wrapped_if_datetimelike(result)
            if isinstance(result, np.ndarray):
                if len(result) == 0 and not was_ndarray:
                    # e.g. empty list
                    return FloatingArray._from_sequence(data, dtype="Float64")
                return NumpyExtensionArray._from_sequence(
                    data, dtype=result.dtype, copy=copy
                )
            if result is data and copy:
                return result.copy()
            return result

        data = cast(np.ndarray, data)
        result = ensure_wrapped_if_datetimelike(data)
        if result is not data:
            result = cast("DatetimeArray | TimedeltaArray", result)
            if copy and result.dtype == data.dtype:
                return result.copy()
            return result

        if data.dtype.kind in "SU":
            # StringArray/ArrowStringArray depending on pd.options.mode.string_storage
            dtype = StringDtype()
            cls = dtype.construct_array_type()
            return cls._from_sequence(data, dtype=dtype, copy=copy)

        elif data.dtype.kind in "iu":
            dtype = IntegerArray._dtype_cls._get_dtype_mapping()[data.dtype]
            return IntegerArray._from_sequence(data, dtype=dtype, copy=copy)
        elif data.dtype.kind == "f":
            # GH#44715 Exclude np.float16 bc FloatingArray does not support it;
            #  we will fall back to NumpyExtensionArray.
            if data.dtype == np.float16:
                return NumpyExtensionArray._from_sequence(
                    data, dtype=data.dtype, copy=copy
                )
            dtype = FloatingArray._dtype_cls._get_dtype_mapping()[data.dtype]
            return FloatingArray._from_sequence(data, dtype=dtype, copy=copy)

        elif data.dtype.kind == "b":
            return BooleanArray._from_sequence(data, dtype="boolean", copy=copy)
        else:
            # e.g. complex
            return NumpyExtensionArray._from_sequence(data, dtype=data.dtype, copy=copy)

    # Pandas overrides NumPy for
    #   1. datetime64[ns,us,ms,s]
    #   2. timedelta64[ns,us,ms,s]
    # so that a DatetimeArray is returned.
    if lib.is_np_dtype(dtype, "M") and is_supported_dtype(dtype):
        return DatetimeArray._from_sequence(data, dtype=dtype, copy=copy)
    if lib.is_np_dtype(dtype, "m") and is_supported_dtype(dtype):
        return TimedeltaArray._from_sequence(data, dtype=dtype, copy=copy)

    elif lib.is_np_dtype(dtype, "mM"):
        raise ValueError(
            # GH#53817
            r"datetime64 and timedelta64 dtype resolutions other than "
            r"'s', 'ms', 'us', and 'ns' are no longer supported."
        )

    return NumpyExtensionArray._from_sequence(data, dtype=dtype, copy=copy)


def array(data, dtype=None, copy=False, order=None,
          mask=nomask, fill_value=None, keep_mask=True,
          hard_mask=False, shrink=True, subok=True, ndmin=0):
    """
    Shortcut to MaskedArray.

    The options are in a different order for convenience and backwards
    compatibility.

    """
    return MaskedArray(data, mask=mask, dtype=dtype, copy=copy,
                       subok=subok, keep_mask=keep_mask,
                       hard_mask=hard_mask, fill_value=fill_value,
                       ndmin=ndmin, shrink=shrink, order=order)


def array(obj, itemsize=None, copy=True, unicode=None, order=None):
    """
    Create a `~numpy.char.chararray`.

    .. deprecated:: 2.5
       ``chararray`` is deprecated. Use an ``ndarray`` with a string or
       bytes dtype instead.

    .. note::
       This class is provided for numarray backward-compatibility.
       New code (not concerned with numarray compatibility) should use
       arrays of type `bytes_` or `str_` and use the free functions
       in :mod:`numpy.char` for fast vectorized string operations instead.

    Versus a NumPy array of dtype `bytes_` or `str_`, this
    class adds the following functionality:

    1) values automatically have whitespace removed from the end
       when indexed

    2) comparison operators automatically remove whitespace from the
       end when comparing values

    3) vectorized string operations are provided as methods
       (e.g. `chararray.endswith <numpy.char.chararray.endswith>`)
       and infix operators (e.g. ``+, *, %``)

    Parameters
    ----------
    obj : array of str or unicode-like

    itemsize : int, optional
        `itemsize` is the number of characters per scalar in the
        resulting array.  If `itemsize` is None, and `obj` is an
        object array or a Python list, the `itemsize` will be
        automatically determined.  If `itemsize` is provided and `obj`
        is of type str or unicode, then the `obj` string will be
        chunked into `itemsize` pieces.

    copy : bool, optional
        If true (default), then the object is copied.  Otherwise, a copy
        will only be made if ``__array__`` returns a copy, if obj is a
        nested sequence, or if a copy is needed to satisfy any of the other
        requirements (`itemsize`, unicode, `order`, etc.).

    unicode : bool, optional
        When true, the resulting `~numpy.char.chararray` can contain Unicode
        characters, when false only 8-bit characters.  If unicode is
        None and `obj` is one of the following:

        - a `~numpy.char.chararray`,
        - an ndarray of type :class:`str_` or :class:`bytes_`
        - a Python :class:`str` or :class:`bytes` object,

        then the unicode setting of the output array will be
        automatically determined.

    order : {'C', 'F', 'A'}, optional
        Specify the order of the array.  If order is 'C' (default), then the
        array will be in C-contiguous order (last-index varies the
        fastest).  If order is 'F', then the returned array
        will be in Fortran-contiguous order (first-index varies the
        fastest).  If order is 'A', then the returned array may
        be in any order (either C-, Fortran-contiguous, or even
        discontiguous).

    Examples
    --------

    >>> import numpy as np
    >>> char_array = np.char.array(['hello', 'world', 'numpy','array'])
    >>> char_array
    chararray(['hello', 'world', 'numpy', 'array'], dtype='<U5')

    """
    if isinstance(obj, (bytes, str)):
        if unicode is None:
            if isinstance(obj, str):
                unicode = True
            else:
                unicode = False

        if itemsize is None:
            itemsize = len(obj)
        shape = len(obj) // itemsize

        return chararray(shape, itemsize=itemsize, unicode=unicode,
                         buffer=obj, order=order)

    if isinstance(obj, (list, tuple)):
        obj = asnarray(obj)

    if isinstance(obj, ndarray) and issubclass(obj.dtype.type, character):
        # If we just have a vanilla chararray, create a chararray
        # view around it.
        if not isinstance(obj, chararray):
            obj = obj.view(chararray)

        if itemsize is None:
            itemsize = obj.itemsize
            # itemsize is in 8-bit chars, so for Unicode, we need
            # to divide by the size of a single Unicode character,
            # which for NumPy is always 4
            if issubclass(obj.dtype.type, str_):
                itemsize //= 4

        if unicode is None:
            if issubclass(obj.dtype.type, str_):
                unicode = True
            else:
                unicode = False

        if unicode:
            dtype = str_
        else:
            dtype = bytes_

        if order is not None:
            obj = asnarray(obj, order=order)
        if (copy or
                (itemsize != obj.itemsize) or
                (not unicode and isinstance(obj, str_)) or
                (unicode and isinstance(obj, bytes_))):
            obj = obj.astype((dtype, int(itemsize)))
        return obj

    if isinstance(obj, ndarray) and issubclass(obj.dtype.type, object):
        if itemsize is None:
            # Since no itemsize was specified, convert the input array to
            # a list so the ndarray constructor will automatically
            # determine the itemsize for us.
            obj = obj.tolist()
            # Fall through to the default case

    if unicode:
        dtype = str_
    else:
        dtype = bytes_

    if itemsize is None:
        val = narray(obj, dtype=dtype, order=order, subok=True)
    else:
        val = narray(obj, dtype=(dtype, itemsize), order=order, subok=True)
    return val.view(chararray)


def array(obj, dtype=None, shape=None, offset=0, strides=None, formats=None,
          names=None, titles=None, aligned=False, byteorder=None, copy=True):
    """
    Construct a record array from a wide-variety of objects.

    A general-purpose record array constructor that dispatches to the
    appropriate `recarray` creation function based on the inputs (see Notes).

    Parameters
    ----------
    obj : any
        Input object. See Notes for details on how various input types are
        treated.
    dtype : data-type, optional
        Valid dtype for array.
    shape : int or tuple of ints, optional
        Shape of each array.
    offset : int, optional
        Position in the file or buffer to start reading from.
    strides : tuple of ints, optional
        Buffer (`buf`) is interpreted according to these strides (strides
        define how many bytes each array element, row, column, etc.
        occupy in memory).
    formats, names, titles, aligned, byteorder :
        If `dtype` is ``None``, these arguments are passed to
        `numpy.format_parser` to construct a dtype. See that function for
        detailed documentation.
    copy : bool, optional
        Whether to copy the input object (True), or to use a reference instead.
        This option only applies when the input is an ndarray or recarray.
        Defaults to True.

    Returns
    -------
    np.recarray
        Record array created from the specified object.

    Notes
    -----
    If `obj` is ``None``, then call the `~numpy.recarray` constructor. If
    `obj` is a string, then call the `fromstring` constructor. If `obj` is a
    list or a tuple, then if the first object is an `~numpy.ndarray`, call
    `fromarrays`, otherwise call `fromrecords`. If `obj` is a
    `~numpy.recarray`, then make a copy of the data in the recarray
    (if ``copy=True``) and use the new formats, names, and titles. If `obj`
    is a file, then call `fromfile`. Finally, if obj is an `ndarray`, then
    return ``obj.view(recarray)``, making a copy of the data if ``copy=True``.

    Examples
    --------
    >>> a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    >>> a
    array([[1, 2, 3],
           [4, 5, 6],
           [7, 8, 9]])

    >>> np.rec.array(a)
    rec.array([[1, 2, 3],
               [4, 5, 6],
               [7, 8, 9]],
              dtype=int64)

    >>> b = [(1, 1), (2, 4), (3, 9)]
    >>> c = np.rec.array(b, formats = ['i2', 'f2'], names = ('x', 'y'))
    >>> c
    rec.array([(1, 1.), (2, 4.), (3, 9.)],
              dtype=[('x', '<i2'), ('y', '<f2')])

    >>> c.x
    array([1, 2, 3], dtype=int16)

    >>> c.y
    array([1.,  4.,  9.], dtype=float16)

    >>> r = np.rec.array(['abc','def'], names=['col1','col2'])
    >>> print(r.col1)
    abc

    >>> r.col1
    array('abc', dtype='<U3')

    >>> r.col2
    array('def', dtype='<U3')
    """

    if ((isinstance(obj, (type(None), str)) or hasattr(obj, 'readinto')) and
           formats is None and dtype is None):
        raise ValueError("Must define formats (or dtype) if object is "
                         "None, string, or an open file")

    kwds = {}
    if dtype is not None:
        dtype = sb.dtype(dtype)
    elif formats is not None:
        dtype = format_parser(formats, names, titles,
                              aligned, byteorder).dtype
    else:
        kwds = {'formats': formats,
                'names': names,
                'titles': titles,
                'aligned': aligned,
                'byteorder': byteorder
                }

    if obj is None:
        if shape is None:
            raise ValueError("Must define a shape if obj is None")
        return recarray(shape, dtype, buf=obj, offset=offset, strides=strides)

    elif isinstance(obj, bytes):
        return fromstring(obj, dtype, shape=shape, offset=offset, **kwds)

    elif isinstance(obj, (list, tuple)):
        if isinstance(obj[0], (tuple, list)):
            return fromrecords(obj, dtype=dtype, shape=shape, **kwds)
        else:
            return fromarrays(obj, dtype=dtype, shape=shape, **kwds)

    elif isinstance(obj, recarray):
        if dtype is not None and (obj.dtype != dtype):
            new = obj.view(dtype)
        else:
            new = obj
        if copy:
            new = new.copy()
        return new

    elif hasattr(obj, 'readinto'):
        return fromfile(obj, dtype=dtype, shape=shape, offset=offset)

    elif isinstance(obj, ndarray):
        if dtype is not None and (obj.dtype != dtype):
            new = obj.view(dtype)
        else:
            new = obj
        if copy:
            new = new.copy()
        return new.view(recarray)

    else:
        interface = getattr(obj, "__array_interface__", None)
        if interface is None or not isinstance(interface, dict):
            raise ValueError("Unknown input type")
        obj = sb.array(obj)
        if dtype is not None and (obj.dtype != dtype):
            obj = obj.view(dtype)
        return obj.view(recarray)


def array(object: Any, dtype: DTypeLike | None = None, *args, copy: bool = True,
          order: str | None = "K", ndmin: int = 0,
          device: xc.Device | Sharding | None = None,
          out_sharding: NamedSharding | P | None = None) -> Array:
  """Convert an object to a JAX array.

  JAX implementation of :func:`numpy.array`.

  Args:
    object: an object that is convertible to an array. This includes JAX
      arrays, NumPy arrays, Python scalars, Python collections like lists
      and tuples, objects with a ``__jax_array__`` method, and objects
      supporting the Python buffer protocol.
    dtype: optionally specify the dtype of the output array. If not
      specified it will be inferred from the input.
    copy: specify whether to force a copy of the input. Default: True.
    order: not implemented in JAX
    ndmin: integer specifying the minimum number of dimensions in the
      output array.
    device: optional :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.
    out_sharding: (optional) :class:`~jax.sharding.PartitionSpec` or :class:`~jax.NamedSharding`
      representing the sharding of the created array (see `explicit sharding`_ for more details).
      This argument exists for consistency with other array creation routines across JAX.
      Specifying both ``out_sharding`` and ``device`` will result in an error.

  Returns:
    A JAX array constructed from the input.

  See also:
    - :func:`jax.numpy.asarray`: like `array`, but by default only copies
      when necessary.
    - :func:`jax.numpy.from_dlpack`: construct a JAX array from an object
      that implements the dlpack interface.
    - :func:`jax.numpy.frombuffer`: construct a JAX array from an object
      that implements the buffer interface.

  Examples:
    Constructing JAX arrays from Python scalars:

    >>> jnp.array(True)
    Array(True, dtype=bool)
    >>> jnp.array(42)
    Array(42, dtype=int32, weak_type=True)
    >>> jnp.array(3.5)
    Array(3.5, dtype=float32, weak_type=True)
    >>> jnp.array(1 + 1j)
    Array(1.+1.j, dtype=complex64, weak_type=True)

    Constructing JAX arrays from Python collections:

    >>> jnp.array([1, 2, 3])  # list of ints -> 1D array
    Array([1, 2, 3], dtype=int32)
    >>> jnp.array([(1, 2, 3), (4, 5, 6)])  # list of tuples of ints -> 2D array
    Array([[1, 2, 3],
           [4, 5, 6]], dtype=int32)
    >>> jnp.array(range(5))
    Array([0, 1, 2, 3, 4], dtype=int32)

    Constructing JAX arrays from NumPy arrays:

    >>> jnp.array(np.linspace(0, 2, 5))
    Array([0. , 0.5, 1. , 1.5, 2. ], dtype=float32)

    Constructing a JAX array via the Python buffer interface, using Python's
    built-in :mod:`array` module.

    >>> from array import array
    >>> pybuffer = array('i', [2, 3, 5, 7])
    >>> jnp.array(pybuffer)
    Array([2, 3, 5, 7], dtype=int32)

  .. _explicit sharding: https://docs.jax.dev/en/latest/parallel.html
  """
  if args:
    if len(args) > 3:
      raise TypeError(f"array() takes at most 5 positional arguments but {len(args) + 2} were given")

    for i, name in enumerate(["copy", "order", "ndmin"]):
      if i < len(args) and [copy, order, ndmin][i] != [True, "K", 0][i]:
        raise TypeError(f"array() got multiple values for argument '{name}'")
    copy, order, ndmin = (list(args) + [copy, order, ndmin][len(args):])[:3]

    deprecations.warn(
        "jax-array-positional-args",
        "Passing the copy, order, and ndmin arguments to jnp.array positionally "
        "is deprecated. Use keyword arguments instead.",
        stacklevel=2)

  if order is not None and order != "K":
    raise NotImplementedError("Only implemented for order='K'")

  # Fast path: if we're not actually doing any conversion, in many cases we
  # can call lax.stage to lift the value into the trace.
  if dtype is None and device is None and out_sharding is None and ndmin == 0:
    if isinstance(object, core.Tracer) and not core.is_concrete(object):
      return lax._array_copy(object) if copy else object
    if isinstance(object, (int, float, complex, np.number)):
      return lax.stage(object)
    if isinstance(object, np.ndarray) and not isinstance(object, np.ma.MaskedArray):
      return lax.stage(object)

  # check if the given dtype is compatible with JAX
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "array")

  # Here we make a judgment call: we only return a weakly-typed array when the
  # input object itself is weakly typed. That ensures asarray(x) is a no-op
  # whenever x is weak, but avoids introducing weak types with something like
  # array([1, 2, 3])
  weak_type = dtype is None and dtypes.is_weakly_typed(object)

  sharding = None
  if device is not None or out_sharding is not None:
    sharding = util.choose_device_or_out_sharding(device, out_sharding, "jnp.array")

  # Use device_put to avoid a copy for ndarray inputs.
  if (not copy and isinstance(object, np.ndarray) and
      (dtype is None or dtype == object.dtype) and (ndmin <= object.ndim) and
      device is None):
    if dtype is not None:
      # If there is an explicit dtype, we've already canonicalized things and
      # device_put should not canonicalize again.
      object = literals.TypedNdArray(object)
    # Keep the output uncommitted.
    return api.device_put(object)

  # String arrays need separate handling because XLA does not support string
  # as a data type.
  if dtype == dtypes.string_dtype or (
      hasattr(object, "dtype") and object.dtype == dtypes.string_dtype
  ):
    return _make_string_array(
        object=object, dtype=dtype, ndmin=ndmin, device=device
    )

  # For Python scalar literals, call coerce_to_array to catch any overflow
  # errors. We don't use dtypes.is_weakly_typed_scalar because we don't want this
  # triggering for traced values. We do this here because it matters whether or
  # not dtype is None. We don't assign the result because we want the raw object
  # to be used for type inference below.
  if isinstance(object, (bool, int, float, complex)):
    _ = dtypes.coerce_to_array(object, dtype)
  elif not isinstance(object, Array):
    # Check if object supports any of the data exchange protocols
    # (except dlpack, see data-apis/array-api#301). If it does,
    # consume the object as jax array and continue (but not return) so
    # that other array() arguments get processed against the input
    # object.
    #
    # Notice that data exchange protocols define dtype in the
    # corresponding data structures and it may not be available as
    # object.dtype. So, we'll resolve the protocols here before
    # evaluating object.dtype.
    m = getattr(object, '__jax_array__', None)
    if m is not None:
      object = m()
    elif hasattr(object, '__cuda_array_interface__'):
      cai = object.__cuda_array_interface__
      backend = xla_bridge.get_backend()
      if 'rocm' in backend.platform_version.lower():
        gpu_plugin_extension = rocm_plugin_extension
      elif 'cuda' in backend.platform_version.lower():
        gpu_plugin_extension = cuda_plugin_extension
      else:
        gpu_plugin_extension = None
      if gpu_plugin_extension is None:
        device_id = None
      else:
        device_id = gpu_plugin_extension.get_device_ordinal(cai["data"][0])
      object = _jax.cuda_array_interface_to_buffer(
          cai=cai, gpu_backend=backend, device_id=device_id)

  # To handle nested lists & tuples, flatten the tree and process each leaf.
  leaves, treedef = tree_util.tree_flatten(
      object, is_leaf=lambda x: not isinstance(x, (list, tuple)))
  if any(leaf is None for leaf in leaves):
    raise ValueError("None is not a valid value for jnp.array")
  leaves = [
      leaf
      if (leaf_jax_array := getattr(leaf, "__jax_array__", None)) is None
      else leaf_jax_array()
      for leaf in leaves
  ]
  if dtype is None:
    # Use lattice_result_type rather than result_type to avoid canonicalization.
    # Otherwise, weakly-typed inputs would have their dtypes canonicalized.
    try:
      dtype = (
          dtypes.lattice_result_type(*leaves)[0]
          if leaves
          else dtypes.default_float_dtype()
      )
    except TypeError:
      # This happens if, e.g. one of the entries is a memoryview object.
      # This is rare, so we only handle it if the normal path fails.
      leaves = [_convert_to_array_if_dtype_fails(leaf) for leaf in leaves]
      dtype = dtypes.lattice_result_type(*leaves)[0]

  object = treedef.unflatten(leaves)
  out: ArrayLike
  if all(not isinstance(leaf, Array) for leaf in leaves):
    # TODO(jakevdp): falling back to numpy here fails to overflow for lists
    # containing large integers; see discussion in
    # https://github.com/jax-ml/jax/pull/6047. More correct would be to call
    # coerce_to_array on each leaf, but this may have performance implications.
    out = np.asarray(object, dtype=dtype)
  elif isinstance(object, Array):
    assert object.aval is not None
    out = lax._array_copy(object) if copy else object
  elif isinstance(object, (list, tuple)):
    if object:
      arrs = (array(elt, dtype=dtype, copy=False) for elt in object)
      arrays_out = [lax.expand_dims(arr, [0]) for arr in arrs]
      # lax.concatenate can be slow to compile for wide concatenations, so form a
      # tree of concatenations as a workaround especially for op-by-op mode.
      # (https://github.com/jax-ml/jax/issues/653).
      k = 16
      while len(arrays_out) > k:
        arrays_out = [lax.concatenate(arrays_out[i:i+k], 0)
                      for i in range(0, len(arrays_out), k)]
      out = lax.concatenate(arrays_out, 0)
    else:
      out = np.array([], dtype=dtype)
  elif _supports_buffer_protocol(object):
    object = memoryview(object)
    # TODO(jakevdp): update this once we support NumPy 2.0 semantics for the copy arg.
    out = np.array(object) if copy else np.asarray(object)
  else:
    raise TypeError(f"Unexpected input type for array: {type(object)}")
  out_array: Array = lax._convert_element_type(
      out, dtype, weak_type=weak_type, sharding=sharding)
  if ndmin > np.ndim(out_array):
    out_array = lax.expand_dims(out_array, range(ndmin - np.ndim(out_array)))
  return out_array

