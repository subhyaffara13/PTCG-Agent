import os

def kronsum(A, B, format=None):
    """Kronecker sum of square sparse matrices `A` and `B`.

    Kronecker sum of two sparse matrices is a sum of two Kronecker
    products ``kron(I_n,A) + kron(B,I_m)`` where `A` has shape ``(m, m)``
    and `B` has shape ``(n, n)`` and ``I_m`` and ``I_n`` are identity matrices
    of shape ``(m, m)`` and ``(n, n)``, respectively.

    .. warning::

        `kronsum` is switching to the sparse array interface.

        For the case where no input arrays are sparse, this function is
        switching to returning a sparse array instead of sparse matrix.
        Control the sparse return class by making at least one input sparse,
        e.g., ``kronsum(coo_matrix(A), B)``, or ``kronsum(coo_array(A), B)``.
        That removes any deprecation warnings as well.
        For more general information about sparrays, see
        :ref:`Migration from spmatrix to sparray <migration_to_sparray>`.
        Handling of this no sparse input case will change no earlier than v1.20.

    Parameters
    ----------
    A : sparse matrix or array
        Square matrix
    B : sparse array or array
        Square matrix
    format : str
        format of the result (e.g. "csr")

    Returns
    -------
    sparse matrix or array
        kronecker sum in a sparse format. Returns a sparse matrix unless either
        `A` or `B` is a sparse array in which case returns a sparse array.

    Examples
    --------
    `kronsum` can be used to construct a finite difference discretization of the 2D
    Laplacian from a 1D discretization.

    >>> from scipy.sparse import diags_array, kronsum
    >>> from matplotlib import pyplot as plt
    >>> import numpy as np
    >>> ex = np.ones(10)
    >>> D_x = diags_array([ex, -ex[1:]], offsets=[0, -1])  # 1D first derivative
    >>> D_xx = D_x.T @ D_x  # 1D second derivative
    >>> L = kronsum(D_xx, D_xx)  # 2D Laplacian
    >>> plt.spy(L.toarray())
    >>> plt.show()

    """
    # TODO: delete this if-clause and replace _sparse with _array when spmatrix removed
    if isinstance(A, sparray) or isinstance(B, sparray):
        # convert to local variables
        coo_sparse = coo_array
        identity_sparse = eye_array
    elif isinstance(A, spmatrix) or isinstance(B, spmatrix):
        coo_sparse = coo_matrix
        identity_sparse = identity
    else:  # all dense
        msg = """`kronsum` is switching to the sparse array interface.

        For the case where input arrays are numpy arrays, this function is
        switching to returning a sparse array instead of sparse matrix.
        Recover the sparse matrix return value by making one input a sparse matrix.
        For example, kronsum(coo_matrix(A), B).
        Avoid this message for sparse array output by using kronsum(coo_array(A), B).
        For more information, see the spmatrix to sparray migration guide
        https://docs.scipy.org/doc/scipy/reference/sparse.migration_to_sparray.html

        This function will be changed no earlier than v1.20.
        """
        prefixes = (os.path.dirname(__file__),)
        warn(msg, category=DeprecationWarning, skip_file_prefixes=prefixes)
        # default when all input are ndarray
        coo_sparse = coo_matrix
        identity_sparse = identity

    A = coo_sparse(A)
    B = coo_sparse(B)

    if A.ndim != 2:
        raise ValueError(f"kronsum requires 2D inputs. `A` is {A.ndim}D.")
    if B.ndim != 2:
        raise ValueError(f"kronsum requires 2D inputs. `B` is {B.ndim}D.")
    if A.shape[0] != A.shape[1]:
        raise ValueError('A is not square')
    if B.shape[0] != B.shape[1]:
        raise ValueError('B is not square')

    dtype = upcast(A.dtype, B.dtype)

    I_n = identity_sparse(A.shape[0], dtype=dtype)
    I_m = identity_sparse(B.shape[0], dtype=dtype)
    L = kron(I_m, A, format='coo')
    R = kron(B, I_n, format='coo')

    return (L + R).asformat(format)

