from typing import Any

def to_numpy(x) -> np.ndarray[Any]:
    if isinstance(x, np.ndarray):
        return x
    elif hasattr(x, "detach"):
        return x.detach().cpu().numpy()
    else:
        return np.array(x)


def to_numpy(obj):
    """
    Convert a PyTorch tensor, Numpy array or python list to a Numpy array.
    """

    framework_to_numpy = {
        "pt": lambda obj: obj.detach().cpu().numpy(),
        "np": lambda obj: obj,
    }

    if isinstance(obj, (dict, UserDict)):
        return {k: to_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return np.array(obj)

    # This gives us a smart order to test the frameworks with the corresponding tests.
    framework_to_test_func = _get_frameworks_and_test_func(obj)
    for framework, test_func in framework_to_test_func.items():
        if test_func(obj):
            return framework_to_numpy[framework](obj)

    return obj


def to_numpy(tensor):
    return tensor.cpu().numpy()


def to_numpy(tensor):
    return tensor.cpu().numpy()


def to_numpy(m, **options):
    """Convert a sympy/scipy.sparse matrix to a numpy matrix."""
    dtype = options.get('dtype', 'complex')
    if isinstance(m, (MatrixBase, Expr)):
        return sympy_to_numpy(m, dtype=dtype)
    elif isinstance(m, numpy_ndarray):
        return m
    elif isinstance(m, scipy_sparse_matrix):
        return m.todense()
    raise TypeError('Expected sympy/numpy/scipy.sparse matrix, got: %r' % m)


def to_numpy(data):
    """Convert to numpy ndarrays."""
    import torch  # noqa: PLC0415

    if not isinstance(data, np.ndarray):
        if not importlib.util.find_spec("torch"):
            logger.error(
                "Please install torch to enable subsequent data type check and conversion, "
                "or reorganize your data format to numpy array."
            )
            exit(0)
        if isinstance(data, torch.Tensor):
            if data.dtype is torch.bfloat16:  # pragma: no cover
                return data.detach().cpu().to(torch.float32).numpy()
            if data.dtype is torch.chalf:  # pragma: no cover
                return data.detach().cpu().to(torch.cfloat).numpy()
            return data.detach().cpu().numpy()
        else:
            try:
                return np.array(data)
            except Exception:
                assert False, (  # noqa: B011
                    f"The input data for onnx model is {type(data)}, which is not supported to convert to numpy ndarrays."
                )
    else:
        return data


def to_numpy(x):
    if isinstance(x, dict):
        return {k: to_numpy(v) for k, v in x.items()}
    elif isinstance(x, list):
        return np.array(x)
    elif isinstance(x, np.ndarray):
        return x
    else:
        return np.array(x)

