from typing import Optional, Union

def to_datetime(
    arg: DatetimeScalar,
    errors: DateTimeErrorChoices = ...,
    dayfirst: bool = ...,
    yearfirst: bool = ...,
    utc: bool = ...,
    format: str | None = ...,
    exact: bool = ...,
    unit: str | None = ...,
    origin=...,
    cache: bool = ...,
) -> Timestamp: ...


def to_datetime(
    arg: Series | DictConvertible,
    errors: DateTimeErrorChoices = ...,
    dayfirst: bool = ...,
    yearfirst: bool = ...,
    utc: bool = ...,
    format: str | None = ...,
    exact: bool = ...,
    unit: str | None = ...,
    origin=...,
    cache: bool = ...,
) -> Series: ...


def to_datetime(
    arg: list | tuple | Index | ArrayLike,
    errors: DateTimeErrorChoices = ...,
    dayfirst: bool = ...,
    yearfirst: bool = ...,
    utc: bool = ...,
    format: str | None = ...,
    exact: bool = ...,
    unit: str | None = ...,
    origin=...,
    cache: bool = ...,
) -> DatetimeIndex: ...


def to_datetime(
    arg: DatetimeScalarOrArrayConvertible | DictConvertible,
    errors: DateTimeErrorChoices = "raise",
    dayfirst: bool = False,
    yearfirst: bool = False,
    utc: bool = False,
    format: str | None = None,
    exact: bool | lib.NoDefault = lib.no_default,
    unit: str | None = None,
    origin: str = "unix",
    cache: bool = True,
) -> DatetimeIndex | Series | DatetimeScalar | NaTType:
    """
    Convert argument to datetime.

    This function converts a scalar, array-like, :class:`Series` or
    :class:`DataFrame`/dict-like to a pandas datetime object.

    Parameters
    ----------
    arg : int, float, str, datetime, list, tuple, 1-d array, Series, DataFrame/dict-like
        The object to convert to a datetime. If a :class:`DataFrame` is provided, the
        method expects minimally the following columns: :const:`"year"`,
        :const:`"month"`, :const:`"day"`. The column "year"
        must be specified in 4-digit format.
    errors : {'raise', 'coerce'}, default 'raise'
        - If :const:`'raise'`, then invalid parsing will raise an exception.
        - If :const:`'coerce'`, then invalid parsing will be set as :const:`NaT`.
    dayfirst : bool, default False
        Specify a date parse order if `arg` is str or is list-like.
        If :const:`True`, parses dates with the day first, e.g. :const:`"10/11/12"`
        is parsed as :const:`2012-11-10`.

        .. warning::

            ``dayfirst=True`` is not strict, but will prefer to parse
            with day first.

    yearfirst : bool, default False
        Specify a date parse order if `arg` is str or is list-like.

        - If :const:`True` parses dates with the year first, e.g.
          :const:`"10/11/12"` is parsed as :const:`2010-11-12`.
        - If both `dayfirst` and `yearfirst` are :const:`True`, `yearfirst` is
          preceded (same as :mod:`dateutil`).

        .. warning::

            ``yearfirst=True`` is not strict, but will prefer to parse
            with year first.

    utc : bool, default False
        Control timezone-related parsing, localization and conversion.

        - If :const:`True`, the function *always* returns a timezone-aware
          UTC-localized :class:`Timestamp`, :class:`Series` or
          :class:`DatetimeIndex`. To do this, timezone-naive inputs are
          *localized* as UTC, while timezone-aware inputs are *converted* to UTC.

        - If :const:`False` (default), inputs will not be coerced to UTC.
          Timezone-naive inputs will remain naive, while timezone-aware ones
          will keep their time offsets. Limitations exist for mixed
          offsets (typically, daylight savings), see :ref:`Examples
          <to_datetime_tz_examples>` section for details.

        See also: pandas general documentation about `timezone conversion and
        localization
        <https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
        #time-zone-handling>`_.

    format : str, default None
        The strftime to parse time, e.g. :const:`"%d/%m/%Y"`. See
        `strftime documentation
        <https://docs.python.org/3/library/datetime.html
        #strftime-and-strptime-behavior>`_ for more information on choices, though
        note that :const:`"%f"` will parse all the way up to nanoseconds.
        You can also pass:

        - "ISO8601", to parse any `ISO8601 <https://en.wikipedia.org/wiki/ISO_8601>`_
          time string (not necessarily in exactly the same format);
        - "mixed", to infer the format for each element individually. This is risky,
          and you should probably use it along with `dayfirst`.

        .. note::

            If a :class:`DataFrame` is passed, then `format` has no effect.

    exact : bool, default True
        Control how `format` is used:

        - If :const:`True`, require an exact `format` match.
        - If :const:`False`, allow the `format` to match anywhere in the target
          string.

        Cannot be used alongside ``format='ISO8601'`` or ``format='mixed'``.
    unit : str, default 'ns'
        The unit of the arg (D,s,ms,us,ns) denote the unit, which is an
        integer or float number. This will be based off the origin.
        Example, with ``unit='ms'`` and ``origin='unix'``, this would calculate
        the number of milliseconds to the unix epoch start.
    origin : scalar, default 'unix'
        Define the reference date. The numeric values would be parsed as number
        of units (defined by `unit`) since this reference date.

        - If :const:`'unix'` (or POSIX) time; origin is set to 1970-01-01.
        - If :const:`'julian'`, unit must be :const:`'D'`, and origin is set to
          beginning of Julian Calendar. Julian day number :const:`0` is assigned
          to the day starting at noon on January 1, 4713 BC.
        - If Timestamp convertible (Timestamp, dt.datetime, np.datetimt64 or date
          string), origin is set to Timestamp identified by origin.
        - If a float or integer, origin is the difference
          (in units determined by the ``unit`` argument) relative to 1970-01-01.
    cache : bool, default True
        If :const:`True`, use a cache of unique, converted dates to apply the
        datetime conversion. May produce significant speed-up when parsing
        duplicate date strings, especially ones with timezone offsets. The cache
        is only used when there are at least 50 values. The presence of
        out-of-bounds values will render the cache unusable and may slow down
        parsing.

    Returns
    -------
    datetime
        If parsing succeeded.
        Return type depends on input (types in parenthesis correspond to
        fallback in case of unsuccessful timezone or out-of-range timestamp
        parsing):

        - scalar: :class:`Timestamp` (or :class:`datetime.datetime`)
        - array-like: :class:`DatetimeIndex` (or :class:`Series` with
          :class:`object` dtype containing :class:`datetime.datetime`)
        - Series: :class:`Series` of :class:`datetime64` dtype (or
          :class:`Series` of :class:`object` dtype containing
          :class:`datetime.datetime`)
        - DataFrame: :class:`Series` of :class:`datetime64` dtype (or
          :class:`Series` of :class:`object` dtype containing
          :class:`datetime.datetime`)

    Raises
    ------
    ParserError
        When parsing a date from string fails.
    ValueError
        When another datetime conversion error happens. For example when one
        of 'year', 'month', day' columns is missing in a :class:`DataFrame`, or
        when a Timezone-aware :class:`datetime.datetime` is found in an array-like
        of mixed time offsets, and ``utc=False``, or when parsing datetimes
        with mixed time zones unless ``utc=True``. If parsing datetimes with mixed
        time zones, please specify ``utc=True``.

    See Also
    --------
    DataFrame.astype : Cast argument to a specified dtype.
    to_timedelta : Convert argument to timedelta.
    convert_dtypes : Convert dtypes.

    Notes
    -----

    Many input types are supported, and lead to different output types:

    - **scalars** can be int, float, str, datetime object (from stdlib :mod:`datetime`
      module or :mod:`numpy`). They are converted to :class:`Timestamp` when
      possible, otherwise they are converted to :class:`datetime.datetime`.
      None/NaN/null scalars are converted to :const:`NaT`.

    - **array-like** can contain int, float, str, datetime objects. They are
      converted to :class:`DatetimeIndex` when possible, otherwise they are
      converted to :class:`Index` with :class:`object` dtype, containing
      :class:`datetime.datetime`. None/NaN/null entries are converted to
      :const:`NaT` in both cases.

    - **Series** are converted to :class:`Series` with :class:`datetime64`
      dtype when possible, otherwise they are converted to :class:`Series` with
      :class:`object` dtype, containing :class:`datetime.datetime`. None/NaN/null
      entries are converted to :const:`NaT` in both cases.

    - **DataFrame/dict-like** are converted to :class:`Series` with
      :class:`datetime64` dtype. For each row a datetime is created from assembling
      the various dataframe columns. Column keys can be common abbreviations
      like ['year', 'month', 'day', 'minute', 'second', 'ms', 'us', 'ns']) or
      plurals of the same.

    The following causes are responsible for :class:`datetime.datetime` objects
    being returned (possibly inside an :class:`Index` or a :class:`Series` with
    :class:`object` dtype) instead of a proper pandas designated type
    (:class:`Timestamp`, :class:`DatetimeIndex` or :class:`Series`
    with :class:`datetime64` dtype):

    - when any input element is before :const:`Timestamp.min` or after
      :const:`Timestamp.max`, see `timestamp limitations
      <https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
      #timeseries-timestamp-limits>`_.

    - when ``utc=False`` (default) and the input is an array-like or
      :class:`Series` containing mixed naive/aware datetime, or aware with mixed
      time offsets. Note that this happens in the (quite frequent) situation when
      the timezone has a daylight savings policy. In that case you may wish to
      use ``utc=True``.

    Examples
    --------

    **Handling various input formats**

    Assembling a datetime from multiple columns of a :class:`DataFrame`. The keys
    can be common abbreviations like ['year', 'month', 'day', 'minute', 'second',
    'ms', 'us', 'ns']) or plurals of the same

    >>> df = pd.DataFrame({"year": [2015, 2016], "month": [2, 3], "day": [4, 5]})
    >>> pd.to_datetime(df)
    0   2015-02-04
    1   2016-03-05
    dtype: datetime64[us]

    Using a unix epoch time

    >>> pd.to_datetime(1490195805, unit="s")
    Timestamp('2017-03-22 15:16:45')
    >>> pd.to_datetime(1490195805433502912, unit="ns")
    Timestamp('2017-03-22 15:16:45.433502912')

    .. warning:: For float arg, precision rounding might happen. To prevent
        unexpected behavior use a fixed-width exact type.

    Using a non-unix epoch origin

    >>> pd.to_datetime([1, 2, 3], unit="D", origin=pd.Timestamp("1960-01-01"))
    DatetimeIndex(['1960-01-02', '1960-01-03', '1960-01-04'],
                  dtype='datetime64[s]', freq=None)

    **Differences with strptime behavior**

    :const:`"%f"` will parse all the way up to nanoseconds.

    >>> pd.to_datetime("2018-10-26 12:00:00.0000000011", format="%Y-%m-%d %H:%M:%S.%f")
    Timestamp('2018-10-26 12:00:00.000000001')

    **Non-convertible date/times**

    Passing ``errors='coerce'`` will force an out-of-bounds date to :const:`NaT`,
    in addition to forcing non-dates (or non-parseable dates) to :const:`NaT`.

    >>> pd.to_datetime("invalid for Ymd", format="%Y%m%d", errors="coerce")
    NaT

    .. _to_datetime_tz_examples:

    **Timezones and time offsets**

    The default behaviour (``utc=False``) is as follows:

    - Timezone-naive inputs are converted to timezone-naive :class:`DatetimeIndex`:

    >>> pd.to_datetime(["2018-10-26 12:00:00", "2018-10-26 13:00:15"])
    DatetimeIndex(['2018-10-26 12:00:00', '2018-10-26 13:00:15'],
                  dtype='datetime64[us]', freq=None)

    - Timezone-aware inputs *with constant time offset* are converted to
      timezone-aware :class:`DatetimeIndex`:

    >>> pd.to_datetime(["2018-10-26 12:00 -0500", "2018-10-26 13:00 -0500"])
    DatetimeIndex(['2018-10-26 12:00:00-05:00', '2018-10-26 13:00:00-05:00'],
                  dtype='datetime64[us, UTC-05:00]', freq=None)

    - However, timezone-aware inputs *with mixed time offsets* (for example
      issued from a timezone with daylight savings, such as Europe/Paris)
      are **not successfully converted** to a :class:`DatetimeIndex`.
      Parsing datetimes with mixed time zones will raise a ValueError unless
      ``utc=True``:

    >>> pd.to_datetime(
    ...     ["2020-10-25 02:00 +0200", "2020-10-25 04:00 +0100"]
    ... )  # doctest: +SKIP
    ValueError: Mixed timezones detected. Pass utc=True in to_datetime
    or tz='UTC' in DatetimeIndex to convert to a common timezone.

    - To create a :class:`Series` with mixed offsets and ``object`` dtype, please use
      :meth:`Series.apply` and :func:`datetime.datetime.strptime`:

    >>> import datetime as dt
    >>> ser = pd.Series(["2020-10-25 02:00 +0200", "2020-10-25 04:00 +0100"])
    >>> ser.apply(lambda x: dt.datetime.strptime(x, "%Y-%m-%d %H:%M %z"))
    0    2020-10-25 02:00:00+02:00
    1    2020-10-25 04:00:00+01:00
    dtype: object

    - A mix of timezone-aware and timezone-naive inputs will also raise a ValueError
      unless ``utc=True``:

    >>> from datetime import datetime
    >>> pd.to_datetime(
    ...     ["2020-01-01 01:00:00-01:00", datetime(2020, 1, 1, 3, 0)]
    ... )  # doctest: +SKIP
    ValueError: Mixed timezones detected. Pass utc=True in to_datetime
    or tz='UTC' in DatetimeIndex to convert to a common timezone.

    |

    Setting ``utc=True`` solves most of the above issues:

    - Timezone-naive inputs are *localized* as UTC

    >>> pd.to_datetime(["2018-10-26 12:00", "2018-10-26 13:00"], utc=True)
    DatetimeIndex(['2018-10-26 12:00:00+00:00', '2018-10-26 13:00:00+00:00'],
                  dtype='datetime64[us, UTC]', freq=None)

    - Timezone-aware inputs are *converted* to UTC (the output represents the
      exact same datetime, but viewed from the UTC time offset `+00:00`).

    >>> pd.to_datetime(["2018-10-26 12:00 -0530", "2018-10-26 12:00 -0500"], utc=True)
    DatetimeIndex(['2018-10-26 17:30:00+00:00', '2018-10-26 17:00:00+00:00'],
                  dtype='datetime64[us, UTC]', freq=None)

    - Inputs can contain both string or datetime, the above
      rules still apply

    >>> pd.to_datetime(["2018-10-26 12:00", datetime(2020, 1, 1, 18)], utc=True)
    DatetimeIndex(['2018-10-26 12:00:00+00:00', '2020-01-01 18:00:00+00:00'],
                  dtype='datetime64[us, UTC]', freq=None)
    """
    if exact is not lib.no_default and format in {"mixed", "ISO8601"}:
        raise ValueError("Cannot use 'exact' when 'format' is 'mixed' or 'ISO8601'")
    if arg is None:
        return NaT

    if origin != "unix":
        arg = _adjust_to_origin(arg, origin, unit)

    convert_listlike = partial(
        _convert_listlike_datetimes,
        utc=utc,
        unit=unit,
        dayfirst=dayfirst,
        yearfirst=yearfirst,
        errors=errors,
        exact=exact,  # type: ignore[arg-type]
    )
    result: Timestamp | NaTType | Series | Index

    if isinstance(arg, Timestamp):
        result = arg
        if utc:
            if arg.tz is not None:
                result = arg.tz_convert("utc")
            else:
                result = arg.tz_localize("utc")
    elif isinstance(arg, ABCSeries):
        cache_array = _maybe_cache(arg, format, cache, convert_listlike)
        if not cache_array.empty:
            result = arg.map(cache_array)
        else:
            values = convert_listlike(arg._values, format)
            result = arg._constructor(values, index=arg.index, name=arg.name)
    elif isinstance(arg, (ABCDataFrame, abc.MutableMapping)):
        result = _assemble_from_unit_mappings(arg, errors, utc)
    elif isinstance(arg, Index):
        cache_array = _maybe_cache(arg, format, cache, convert_listlike)
        if not cache_array.empty:
            result = _convert_and_box_cache(arg, cache_array, name=arg.name)
        else:
            result = convert_listlike(arg, format, name=arg.name)
    elif is_list_like(arg):
        try:
            # error: Argument 1 to "_maybe_cache" has incompatible type
            # "Union[float, str, datetime, List[Any], Tuple[Any, ...], ExtensionArray,
            # ndarray[Any, Any], Series]"; expected "Union[List[Any], Tuple[Any, ...],
            # Union[Union[ExtensionArray, ndarray[Any, Any]], Index, Series], Series]"
            argc = cast(
                Union[list, tuple, ExtensionArray, np.ndarray, "Series", Index], arg
            )
            cache_array = _maybe_cache(argc, format, cache, convert_listlike)
        except OutOfBoundsDatetime:
            # caching attempts to create a DatetimeIndex, which may raise
            # an OOB. If that's the desired behavior, then just reraise...
            if errors == "raise":
                raise
            # ... otherwise, continue without the cache.
            from pandas import Series

            cache_array = Series([], dtype=object)  # just an empty array
        if not cache_array.empty:
            result = _convert_and_box_cache(argc, cache_array)
        else:
            result = convert_listlike(argc, format)
    else:
        result = convert_listlike(np.array([arg]), format)[0]
        if isinstance(arg, bool) and isinstance(result, np.bool_):
            result = bool(result)  # TODO: avoid this kludge.

    #  error: Incompatible return value type (got "Union[Timestamp, NaTType,
    # Series, Index]", expected "Union[DatetimeIndex, Series, float, str,
    # NaTType, None]")
    return result  # type: ignore[return-value]


def to_datetime(
    ts: Timestamp, tz: Optional[datetime.tzinfo] = None
) -> datetime.datetime:
  """Converts Timestamp to a datetime.

  Args:
    tz: A datetime.tzinfo subclass; defaults to None.

  Returns:
    If tzinfo is None, returns a timezone-naive UTC datetime (with no timezone
    information, i.e. not aware that it's UTC).

    Otherwise, returns a timezone-aware datetime in the input timezone.
  """
  return ts.ToDatetime(tzinfo=tz)

