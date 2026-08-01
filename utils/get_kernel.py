
def get_kernel(
    op: _op_identifier, dispatch_key: str | torch.DispatchKey
) -> torch._C._SafeKernelFunction:
    """Returns the computed kernel for a given operator and dispatch key.

    This function retrieves the kernel that would be executed for a given
    operator and dispatch key combination. The returned SafeKernelFunction
    can be used to call the kernel in a boxed fashion. The intended use
    case for this function is to retrieve the original kernel for a given
    dispatch key and then register another kernel to the same dispatch key
    that calls into the original kernel for certain cases.

    Args:
        op: Operator name (along with the overload) or OpOverload object
            Can be a string (e.g., "aten::add.Tensor"), an OpOverload, or a CustomOpDef.
        dispatch_key (str | torch.DispatchKey): The dispatch key to get the kernel for.
            Can be a string (e.g., "CPU", "CUDA") or a DispatchKey enum value.

    Returns:
        torch._C._SafeKernelFunction: A safe kernel function that can be used to
            call the kernel.

    Raises:
        RuntimeError: If the operator does not exist.

    Example:
        >>> # Get the CPU kernel for torch.add
        >>> kernel = torch.library.get_kernel("aten::add.Tensor", "CPU")
        >>>
        >>> # You can also use DispatchKey enum
        >>> kernel = torch.library.get_kernel("aten::add.Tensor", torch.DispatchKey.CPU)
        >>>
        >>> # Or use an OpOverload directly
        >>> kernel = torch.library.get_kernel(torch.ops.aten.add.Tensor, "CPU")
        >>>
        >>> # Example: Using get_kernel in a custom op with conditional dispatch
        >>> # Get the original kernel for torch.sin
        >>> original_sin_kernel = torch.library.get_kernel("aten::sin", "CPU")
        >>>
        >>> # If input has negative values, use original sin, otherwise return zeros
        >>> def conditional_sin_impl(dispatch_keys, x):
        >>>     if (x < 0).any():
        >>>         return original_sin_kernel.call_boxed(dispatch_keys, x)
        >>>     else:
        >>>         return torch.zeros_like(x)
        >>>
        >>> lib = torch.library.Library("aten", "IMPL")
        >>> # with_keyset=True so the first argument to the impl is the current DispatchKeySet
        >>> which needs to be the first argument to ``kernel.call_boxed``
        >>> lib.impl("sin", conditional_sin_impl, "CPU", with_keyset=True)
        >>>
        >>> # Test the conditional behavior
        >>> x_positive = torch.tensor([1.0, 2.0])
        >>> x_mixed = torch.tensor([-1.0, 2.0])
        >>> torch.sin(x_positive)
        tensor([0., 0.])
        >>> torch.sin(x_mixed)
        tensor([-0.8415, 0.9093])
    """
    if not isinstance(op, (str, torch._ops.OpOverload)):
        raise ValueError(f"get_kernel({op}): got unexpected type for op: {type(op)}")

    if isinstance(op, torch._ops.OpOverload):
        op = op._name

    if isinstance(dispatch_key, str):
        try:
            dispatch_key = torch._C.DispatchKey.__members__[dispatch_key]
        except KeyError:
            raise ValueError(f"Invalid dispatch key: {dispatch_key}") from None

    return torch._C._dispatch_get_computed_kernel_for_dispatch_key(op, dispatch_key)


def get_kernel(
    kernel_name: str,
    revision: str | None = None,
    version: int | str | None = None,
    allow_all_kernels: bool = False,
) -> ModuleType:
    from .. import __version__

    if not _kernels_available:
        raise ImportError(
            "`kernels` is either not installed or uses an incompatible version. Please install the latest version "
            "with `pip install -U kernels`."
        )

    repo_parent = kernel_name.split("/")[0]
    # all `kernels-community` repos are trusted by default!
    if repo_parent != "kernels-community" and not allow_all_kernels:
        raise ValueError(
            "You need to specify `allow_all_kernels=True` to use kernels outside of the `kernels-community` repository"
        )

    user_agent = {"framework": "transformers", "version": __version__, "repo_id": kernel_name}
    kernels_version = importlib.metadata.version("kernels")
    if pkg_version.parse(kernels_version) >= pkg_version.parse("0.10.4"):
        return get_kernel_hub(kernel_name, revision=revision, version=version, user_agent=user_agent)
    else:
        return get_kernel_hub(kernel_name, revision=revision, version=version)


def get_kernel(kernel_idx: int) -> "TritonKernelType":
    return kernel_side_table.get_kernel(kernel_idx)

