
def _symeig(
    input,
    eigenvectors=False,
    upper=True,
    *,
    out=None,
) -> tuple[Tensor, Tensor]:
    raise RuntimeError(
        "This function was deprecated since version 1.9 and is now removed. "
        "The default behavior has changed from using the upper triangular portion of the matrix by default "
        "to using the lower triangular portion.\n\n"
        "L, _ = torch.symeig(A, upper=upper) "
        "should be replaced with:\n"
        "L = torch.linalg.eigvalsh(A, UPLO='U' if upper else 'L')\n\n"
        "and\n\n"
        "L, V = torch.symeig(A, eigenvectors=True) "
        "should be replaced with:\n"
        "L, V = torch.linalg.eigh(A, UPLO='U' if upper else 'L')"
    )

