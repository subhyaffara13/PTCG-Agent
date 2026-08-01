
def _getdtype(dtype_str: str) -> np.dtype:
    return _TYPES[dtype_str]


def _getdtype(dtype_str: str) -> paddle.dtype:
    return _TYPES[dtype_str]


def _getdtype(dtype_str: str) -> torch.dtype:
    return _TYPES[dtype_str]

