
def _check_tensor_all(cond, message=None):  # noqa: F811
    r"""Throws error containing an optional message if the specified condition
    is False.

    Error type: ``RuntimeError``

    C++ equivalent: ``TORCH_CHECK_TENSOR_ALL``

    Args:
        cond (:class:`torch.Tensor`): Tensor of dtype ``torch.bool``. If any
            element is ``False``, throw error

        message (Callable, optional): Callable that returns either a string or
            an object that has a ``__str__()`` method to be used as the error
            message. Default: ``None``
    """
    _check_tensor_all_with(RuntimeError, cond, message)

