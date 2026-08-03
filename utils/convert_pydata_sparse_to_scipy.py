from typing import Any

def convert_pydata_sparse_to_scipy(
    arg: Any,
    target_format: None | Literal["csc", "csr"] = None,
    accept_fv: Any = None,
) -> "sp.spmatrix | Any":
    """
    Convert a pydata/sparse array to scipy sparse matrix,
    pass through anything else.
    """
    if is_pydata_spmatrix(arg):
        # The `accept_fv` keyword is new in PyData Sparse 0.15.4 (May 2024),
        # remove the `except` once the minimum supported version is >=0.15.4
        try:
            arg = arg.to_scipy_sparse(accept_fv=accept_fv)
        except TypeError:
            arg = arg.to_scipy_sparse()
        if target_format is not None:
            arg = arg.asformat(target_format)
        elif arg.format not in ("csc", "csr"):
            arg = arg.tocsc()
    return arg

