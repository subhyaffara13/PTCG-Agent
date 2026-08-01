
def is_tensor(obj: _Any, /) -> _TypeIs["torch.Tensor"]:
    r"""Returns True if `obj` is a PyTorch tensor.

    Args:
        obj (object): Object to test
    Example::

        >>> x = torch.tensor([1, 2, 3])
        >>> torch.is_tensor(x)
        True

    """
    return isinstance(obj, torch.Tensor)


def is_tensor(typ: Type) -> bool:
    return isinstance(typ, BaseType) and typ.name == BaseTy.Tensor


def is_tensor(x) -> bool:
    """
    Tests if `x` is a `torch.Tensor`, `np.ndarray` or `mlx.array` in the order defined by `infer_framework_from_repr`
    """
    # This gives us a smart order to test the frameworks with the corresponding tests.
    framework_to_test_func = _get_frameworks_and_test_func(x)
    for test_func in framework_to_test_func.values():
        if test_func(x):
            return True

    # Tracers
    if is_torch_fx_proxy(x):
        return True

    return False


def is_tensor(ann) -> bool:
    if issubclass(ann, torch.Tensor):
        return True

    if issubclass(
        ann,
        (
            torch.LongTensor,
            torch.DoubleTensor,
            torch.FloatTensor,
            torch.IntTensor,
            torch.ShortTensor,
            torch.HalfTensor,
            torch.CharTensor,
            torch.ByteTensor,
            torch.BoolTensor,
        ),
    ):
        warnings.warn(
            "TorchScript will treat type annotations of Tensor "
            "dtype-specific subtypes as if they are normal Tensors. "
            "dtype constraints are not enforced in compilation either.",
            stacklevel=2,
        )
        return True

    return False

