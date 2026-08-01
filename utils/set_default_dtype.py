
def set_default_dtype(d: "torch.dtype", /) -> None:
    r"""

    Sets the default floating point dtype to :attr:`d`. Supports floating point dtype
    as inputs. Other dtypes will cause torch to raise an exception.

    When PyTorch is initialized its default floating point dtype is torch.float32,
    and the intent of set_default_dtype(torch.float64) is to facilitate NumPy-like
    type inference. The default floating point dtype is used to:

    1. Implicitly determine the default complex dtype. When the default floating type is float16,
       the default complex dtype is complex32. For float32, the default complex dtype is complex64.
       For float64, it is complex128. For bfloat16, an exception will be raised because
       there is no corresponding complex type for bfloat16.
    2. Infer the dtype for tensors constructed using Python floats or complex Python
       numbers. See examples below.
    3. Determine the result of type promotion between bool and integer tensors and
       Python floats and complex Python numbers.

    Args:
        d (:class:`torch.dtype`): the floating point dtype to make the default.

    Example:
        >>> # xdoctest: +SKIP("Other tests may have changed the default type. Can we reset it?")
        >>> # initial default for floating point is torch.float32
        >>> # Python floats are interpreted as float32
        >>> torch.tensor([1.2, 3]).dtype
        torch.float32
        >>> # initial default for floating point is torch.complex64
        >>> # Complex Python numbers are interpreted as complex64
        >>> torch.tensor([1.2, 3j]).dtype
        torch.complex64

        >>> torch.set_default_dtype(torch.float64)
        >>> # Python floats are now interpreted as float64
        >>> torch.tensor([1.2, 3]).dtype  # a new floating point tensor
        torch.float64
        >>> # Complex Python numbers are now interpreted as complex128
        >>> torch.tensor([1.2, 3j]).dtype  # a new complex tensor
        torch.complex128

        >>> torch.set_default_dtype(torch.float16)
        >>> # Python floats are now interpreted as float16
        >>> torch.tensor([1.2, 3]).dtype  # a new floating point tensor
        torch.float16
        >>> # Complex Python numbers are now interpreted as complex128
        >>> torch.tensor([1.2, 3j]).dtype  # a new complex tensor
        torch.complex32

    """
    _C._set_default_dtype(d)


def set_default_dtype(fp_dtype="numpy", int_dtype="numpy"):
    """Set the (global) defaults for fp, complex, and int dtypes.

    The complex dtype is inferred from the float (fp) dtype. It has
    a width at least twice the width of the float dtype,
    i.e., it's complex128 for float64 and complex64 for float32.

    Parameters
    ----------
    fp_dtype
        Allowed values are "numpy", "pytorch" or dtype_like things which
        can be converted into a DType instance.
        Default is "numpy" (i.e. float64).
    int_dtype
        Allowed values are "numpy", "pytorch" or dtype_like things which
        can be converted into a DType instance.
        Default is "numpy" (i.e. int64).

    Returns
    -------
    The old default dtype state: a namedtuple with attributes ``float_dtype``,
    ``complex_dtypes`` and ``int_dtype``. These attributes store *pytorch*
    dtypes.

    Notes
    ------------
    This functions has a side effect: it sets the global state with the provided dtypes.

    The complex dtype has bit width of at least twice the width of the float
    dtype, i.e. it's complex128 for float64 and complex64 for float32.

    """
    if fp_dtype not in ["numpy", "pytorch"]:
        fp_dtype = dtype(fp_dtype).torch_dtype
    if int_dtype not in ["numpy", "pytorch"]:
        int_dtype = dtype(int_dtype).torch_dtype

    if fp_dtype == "numpy":
        float_dtype = torch.float64
    elif fp_dtype == "pytorch":
        float_dtype = torch.float32
    else:
        float_dtype = fp_dtype

    complex_dtype = {
        torch.float64: torch.complex128,
        torch.float32: torch.complex64,
        torch.float16: torch.complex64,
    }[float_dtype]

    if int_dtype in ["numpy", "pytorch"]:
        int_dtype = torch.int64

    new_defaults = _dtypes_impl.DefaultDTypes(
        float_dtype=float_dtype, complex_dtype=complex_dtype, int_dtype=int_dtype
    )

    # set the new global state and return the old state
    old_defaults = _dtypes_impl.default_dtypes
    _dtypes_impl._default_dtypes = new_defaults
    return old_defaults


def set_default_dtype(dtype):
    saved_dtype = torch.get_default_dtype()
    torch.set_default_dtype(dtype)
    try:
        yield
    finally:
        torch.set_default_dtype(saved_dtype)

