
def set_default_tensor_type(t: type["torch.Tensor"] | str, /) -> None:
    r"""
    .. warning::

        This function is deprecated as of PyTorch 2.1, please use :func:`torch.set_default_dtype()` and
        :func:`torch.set_default_device()` as alternatives.

    Sets the default ``torch.Tensor`` type to floating point tensor type
    ``t``. This type will also be used as default floating point type for
    type inference in :func:`torch.tensor`.

    The default floating point tensor type is initially ``torch.FloatTensor``.

    Args:
        t (type or string): the floating point tensor type or its name

    Example::

        >>> # xdoctest: +SKIP("Other tests may have changed the default type. Can we reset it?")
        >>> torch.tensor([1.2, 3]).dtype    # initial default for floating point is torch.float32
        torch.float32
        >>> torch.set_default_tensor_type(torch.DoubleTensor)
        >>> torch.tensor([1.2, 3]).dtype    # a new floating point tensor
        torch.float64

    """
    if isinstance(t, str):
        t = _import_dotted_name(t)
    _C._set_default_tensor_type(t)


def set_default_tensor_type(tensor_type):
    saved_tensor_type = torch.tensor([]).type()
    torch.set_default_tensor_type(tensor_type)
    try:
        yield
    finally:
        torch.set_default_tensor_type(saved_tensor_type)

