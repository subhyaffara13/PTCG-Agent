from typing import Any

def np_can_hold_element(dtype: np.dtype, element: Any) -> Any:
    """
    Raise if we cannot losslessly set this element into an ndarray with this dtype.

    Specifically about places where we disagree with numpy.  i.e. there are
    cases where numpy will raise in doing the setitem that we do not check
    for here, e.g. setting str "X" into a numeric ndarray.

    Returns
    -------
    Any
        The element, potentially cast to the dtype.

    Raises
    ------
    ValueError : If we cannot losslessly store this element with this dtype.
    """
    if dtype == _dtype_obj:
        return element

    tipo = _maybe_infer_dtype_type(element)

    if dtype.kind in "iu":
        if isinstance(element, range):
            if _dtype_can_hold_range(element, dtype):
                return element
            raise LossySetitemError

        if is_integer(element) or (is_float(element) and element.is_integer()):
            # e.g. test_setitem_series_int8 if we have a python int 1
            #  tipo may be np.int32, despite the fact that it will fit
            #  in smaller int dtypes.
            info = np.iinfo(dtype)
            if info.min <= element <= info.max:
                return dtype.type(element)
            raise LossySetitemError

        if tipo is not None:
            if tipo.kind not in "iu":
                if isinstance(element, np.ndarray) and element.dtype.kind == "f":
                    # If all can be losslessly cast to integers, then we can hold them
                    with np.errstate(invalid="ignore"):
                        # We check afterwards if cast was losslessly, so no need to show
                        # the warning
                        casted = element.astype(dtype)
                    comp = casted == element
                    if comp.all():
                        # Return the casted values bc they can be passed to
                        #  np.putmask, whereas the raw values cannot.
                        #  see TestSetitemFloatNDarrayIntoIntegerSeries
                        return casted
                    raise LossySetitemError

                elif isinstance(element, ABCExtensionArray) and isinstance(
                    element.dtype, CategoricalDtype
                ):
                    # GH#52927 setting Categorical value into non-EA frame
                    # TODO: general-case for EAs?
                    try:
                        casted = element.astype(dtype)
                    except (ValueError, TypeError) as err:
                        raise LossySetitemError from err
                    # Check for cases of either
                    #  a) lossy overflow/rounding or
                    #  b) semantic changes like dt64->int64
                    comp = casted == element
                    if not comp.all():
                        raise LossySetitemError
                    return casted

                # Anything other than integer we cannot hold
                raise LossySetitemError
            if (
                dtype.kind == "u"
                and isinstance(element, np.ndarray)
                and element.dtype.kind == "i"
            ):
                # see test_where_uint64
                casted = element.astype(dtype)
                if (casted == element).all():
                    # TODO: faster to check (element >=0).all()?  potential
                    #  itemsize issues there?
                    return casted
                raise LossySetitemError
            if dtype.itemsize < tipo.itemsize:
                raise LossySetitemError
            if not isinstance(tipo, np.dtype):
                # i.e. nullable IntegerDtype; we can put this into an ndarray
                #  losslessly iff it has no NAs
                arr = element._values if isinstance(element, ABCSeries) else element
                if arr._hasna:
                    raise LossySetitemError
                return element

            return element

        raise LossySetitemError

    if dtype.kind == "f":
        if lib.is_integer(element) or lib.is_float(element):
            casted = dtype.type(element)
            if np.isnan(casted) or casted == element:
                return casted
            # otherwise e.g. overflow see TestCoercionFloat32
            raise LossySetitemError

        if tipo is not None:
            # TODO: itemsize check?

            if isinstance(tipo, CategoricalDtype):
                # GH#56376
                if tipo.categories.dtype.kind not in "iuf":
                    # Anything other than float/integer we cannot hold
                    raise LossySetitemError
                casted = np.asarray(element, dtype=dtype)
                if np.array_equal(casted, element, equal_nan=True):
                    return casted
                raise LossySetitemError

            if tipo.kind not in "iuf":
                # Anything other than float/integer we cannot hold
                raise LossySetitemError
            if not isinstance(tipo, np.dtype):
                # i.e. nullable IntegerDtype or FloatingDtype;
                #  we can put this into an ndarray losslessly iff it has no NAs
                if element._hasna:
                    raise LossySetitemError
                return element
            elif tipo.itemsize > dtype.itemsize or tipo.kind != dtype.kind:
                if isinstance(element, np.ndarray):
                    # e.g. TestDataFrameIndexingWhere::test_where_alignment
                    casted = element.astype(dtype)
                    if np.array_equal(casted, element, equal_nan=True):
                        return casted
                    raise LossySetitemError

            return element

        raise LossySetitemError

    if dtype.kind == "c":
        if lib.is_integer(element) or lib.is_complex(element) or lib.is_float(element):
            if np.isnan(element):
                # see test_where_complex GH#6345
                return dtype.type(element)

            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                casted = dtype.type(element)
            if casted == element:
                return casted
            # otherwise e.g. overflow see test_32878_complex_itemsize
            raise LossySetitemError

        if tipo is not None:
            if tipo.kind in "iufc":
                return element
            raise LossySetitemError
        raise LossySetitemError

    if dtype.kind == "b":
        if tipo is not None:
            if tipo.kind == "b":
                if not isinstance(tipo, np.dtype):
                    # i.e. we have a BooleanArray
                    if element._hasna:
                        # i.e. there are pd.NA elements
                        raise LossySetitemError
                return element
            # GH 57338 check boolean array set as object type
            if tipo.kind == "O" and isinstance(element, np.ndarray):
                if lib.is_bool_array(element):
                    return element.astype("bool")
            raise LossySetitemError
        if lib.is_bool(element):
            return element
        raise LossySetitemError

    if dtype.kind == "S":
        # TODO: test tests.frame.methods.test_replace tests get here,
        #  need more targeted tests.  xref phofl has a PR about this
        if tipo is not None:
            if tipo.kind == "S" and tipo.itemsize <= dtype.itemsize:
                return element
            raise LossySetitemError
        if isinstance(element, bytes) and len(element) <= dtype.itemsize:
            return element
        raise LossySetitemError

    if dtype.kind == "V":
        # i.e. np.void, which cannot hold _anything_
        raise LossySetitemError

    raise NotImplementedError(dtype)

