
def load_and_register_msa_kernel(attn_implementation: str):
    """Load the MSA hub kernel once and verify the expected callables are present.

    The ``attn_implementation`` string may carry a ``paged|`` prefix and/or an ``@<revision>`` pin
    (e.g. ``kernels-staging/msa@v0``); the build currently lives on the repo's ``v0`` branch. The
    loaded module is cached in a module-level global so registration happens once, not per call.
    """
    global _MSA_KERNEL
    if _MSA_KERNEL is not None:
        return _MSA_KERNEL

    from .hub_kernels import get_kernel

    repo_id = attn_implementation.split("|")[-1]
    repo_id, _, rev = repo_id.partition("@")
    kernel = get_kernel(repo_id, revision=rev or None, version=None if rev else 0, allow_all_kernels=True)

    for fn_name in ("sparse_atten_func", "build_k2q_csr"):
        if not callable(getattr(kernel, fn_name, None)):
            raise ImportError(
                f"The MSA kernel loaded from `{repo_id}` does not expose a callable `{fn_name}`. "
                "Make sure you request a compatible build, e.g. `kernels-staging/msa@v0`."
            )

    _MSA_KERNEL = kernel
    return _MSA_KERNEL

